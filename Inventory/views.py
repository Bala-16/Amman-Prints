from urllib import request
from django.db import models
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.db.models import Max, Sum
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .forms import QuotationForm, QuotationItemForm
from .models import Quotation, QuotationItem, JobCard, Party
from .forms import PartyForm
from .utils import generate_doc_no
from django.contrib.auth.decorators import login_required

import json
from datetime import datetime , timedelta

from .models import JobCard

from decimal import Decimal, InvalidOperation


# ============================================================================
# NAVIGATION & BASIC PAGES
# ============================================================================

def nav(request):
    return render(request, 'nav.html')

def customer_report(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    customer_name = request.GET.get('customer_name', '').strip()
    
    # Get all jobcards
    jobcards = JobCard.objects.all()
    
    # DEFAULT: Show only TODAY's data
    today = timezone.now().date()
    
    # If NO filters provided → Show only TODAY
    if not from_date and not to_date and not customer_name:
        jobcards = jobcards.filter(date__date=today)
    else:
        # If ANY filter is provided → Apply filters
        if customer_name:
            jobcards = jobcards.filter(customer_name__icontains=customer_name)
        
        if from_date:
            jobcards = jobcards.filter(date__date__gte=from_date)
        
        if to_date:
            jobcards = jobcards.filter(date__date__lte=to_date)
    
    # Order by date descending (newest first)
    jobcards = jobcards.order_by('-date')
    
    # Prepare report data
    report_data = []
    
    for jc in jobcards:
        # Get items from JSON field
        items = jc.items or []
        
        for item in items:
            qty = item.get('qty', 0) or 0
            confirmed_rate = item.get('confirmed_rate', 0) or item.get('confirmed_amt', 0)
            value = item.get('value', 0) or 0
            
            report_data.append({
                'date': jc.date,
                'jobcard_no': jc.jobcard_no,
                'customer_name': jc.customer_name,
                'particulars': item.get('particulars', ''),
                'quantity': qty,
                'confirmed_rate': confirmed_rate,
                'amt': value,
                'bill_no': jc.jobcard_no,  # Jobcard no as bill no
                'bill_date': jc.date,
            })
    
    context = {
        'report_data': report_data,
        'from_date': from_date or '',
        'to_date': to_date or '',
        'customer_name': customer_name,
        'showing_today': not (from_date or to_date or customer_name),
    }
    
    return render(request, 'jobcard/customer_report.html', context)

def designer_report(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    designer_name = request.GET.get('designer_name', '').strip()
    
    # Get all jobcards
    jobcards = JobCard.objects.all()
    
    # DEFAULT: Show only TODAY's data
    today = timezone.now().date()
    
    # If NO filters provided → Show only TODAY
    if not from_date and not to_date and not designer_name:
        jobcards = jobcards.filter(date__date=today)
    else:
        # If ANY filter is provided → Apply filters
        if designer_name:
            jobcards = jobcards.filter(designer_name__icontains=designer_name)
        
        if from_date:
            jobcards = jobcards.filter(date__date__gte=from_date)
        
        if to_date:
            jobcards = jobcards.filter(date__date__lte=to_date)
    
    # Order by date descending (newest first)
    jobcards = jobcards.order_by('-date')
    
    # Prepare report data
    report_data = []
    total_pcs = 0
    total_value = 0
    s_no = 1
    
    for jc in jobcards:
        # Get items from JSON field
        items = jc.items or []
        
        for item in items:
            qty = item.get('qty', 0) or 0
            value = item.get('value', 0) or 0
            
            report_data.append({
                's_no': s_no,
                'date': jc.date,
                'jobcard_no': jc.jobcard_no,
                'customer_name': jc.customer_name,
                'designer': jc.designer_name,
                'design_name': jc.style_name,
                'no_of_pcs': qty,
                'sample_value': value,
            })
            
            total_pcs += qty
            total_value += value
            s_no += 1
    
    context = {
        'report_data': report_data,
        'total_pcs': total_pcs,
        'total_value': total_value,
        'from_date': from_date or '',
        'to_date': to_date or '',
        'designer_name': designer_name,
        'showing_today': not (from_date or to_date or designer_name),  # For UI message
    }
    
    return render(request, 'jobcard/designer_report.html', context)

def process_report(request):
    return render(request, 'jobcard/process_report.html')

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def login(request):
    return render(request, 'login.html')


# ============================================================================
# JOBCARD API VIEWS - ✅ FIXED & OPTIMIZED
# ============================================================================

def jobcard_form_view(request):
    """Render the jobcard form page"""
    return render(request, 'jobcard/jobcard_form.html')

@csrf_exempt
@require_http_methods(["GET"])
def get_jobcards(request):
    try:
        jobcards = JobCard.objects.all().order_by('-created_at')
        data = []

        for jc in jobcards:
            data.append({
                'id': jc.id,
                'jobcardNo': jc.jobcard_no,
                'date': jc.date.isoformat() if jc.date else '',
                'orderBy': jc.order_by or '',
                'customerName': jc.customer_name or '',
                'jobCreatedBy': jc.job_created_by or 'admin',
                'styleNo': jc.style_no or '',
                'styleName': jc.style_name or '',
                'customerPONo': jc.customer_po_no or '',
                'combo': jc.combo or '',
                'jobType': jc.job_type or '',
                'fabricType': jc.fabric_type or 'N/A',
                'designerName': jc.designer_name or '',
                'hsnCode': jc.hsn_code or '998821',
                'mistakeDetails': jc.mistake_details or '',
                'reason': jc.reason or '',
                'items': jc.items or [],

                # ✅ Decimal to float (IMPORTANT)
                'totalQty': float(jc.total_qty or 0),
                'totalValue': float(jc.total_value or 0),
                'avgRate': float(jc.avg_rate or 0),
                'lConfirmRate': float(jc.l_confirm_rate or 0),
                'hConfirmRate': float(jc.h_confirm_rate or 0),

                'approval': jc.approval or 'Pending',
                'status': jc.status or 'Pending',
                'created_at': jc.created_at.isoformat() if jc.created_at else '',
            })

        return JsonResponse({'jobcards': data})

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def create_jobcard(request):
    """Create new jobcard - API Endpoint"""
    try:
        data = json.loads(request.body)
        
        # Generate Jobcard Number
        now = datetime.now()
        year = now.strftime('%y')
        month = now.strftime('%m')
        
        last_jobcard = JobCard.objects.filter(
            jobcard_no__startswith=f'JC-{year}{month}-'
        ).order_by('-jobcard_no').first()
        
        if last_jobcard:
            last_seq = int(last_jobcard.jobcard_no.split('-')[2])
            sequence = str(last_seq + 1).zfill(4)
        else:
            sequence = '0001'
        
        jobcard_no = f'JC-{year}{month}-{sequence}'
        
        # Process items
        items = data.get('items', [])
        calculated_items = []
        
        for item in items:
            width = float(item.get('width', 0) or 0)
            height = float(item.get('height', 0) or 0)
            rate = float(item.get('rate', 0) or 0)
            confirmed_amt = float(item.get('confirmedAmt', 0) or 0)
            qty = int(item.get('qty', 1) or 1)
            
            sq_inch = width * height
            amt = sq_inch * rate
            confirmed_rate = confirmed_amt / sq_inch if sq_inch != 0 else 0
            value = confirmed_amt * qty
            
            calculated_items.append({
                'particulars': item.get('particulars', ''),
                'width': width,
                'height': height,
                'rate': rate,
                'qty': qty,
                'sq_inch': round(sq_inch, 2),
                'amt': round(amt, 2),
                'confirmed_amt': round(confirmed_amt, 2),
                'confirmed_rate': round(confirmed_rate, 4),
                'value': round(value, 2),
            })
        
        # Calculate totals
        total_qty = sum(i['qty'] for i in calculated_items)
        total_value = sum(i['value'] for i in calculated_items)
        avg_rate = sum(i['rate'] for i in calculated_items) / len(calculated_items) if calculated_items else 0
        
        # Parse date
        date_str = data.get('date', '')
        try:
            if 'Z' in date_str:
                job_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            else:
                job_date = datetime.fromisoformat(date_str)
        except:
            job_date = datetime.now()
        
        # Create JobCard
        jobcard = JobCard.objects.create(
            jobcard_no=jobcard_no,
            date=job_date,
            order_by=data.get('orderBy', ''),
            customer_name=data.get('customerName', ''),
            style_no=data.get('styleNo', ''),
            job_created_by=data.get('jobCreatedBy', 'admin'),
            style_name=data.get('styleName', ''),
            customer_po_no=data.get('customerPONo', ''),
            combo=data.get('combo', ''),
            job_type=data.get('jobType', ''),
            fabric_type=data.get('fabricType', 'N/A'),
            designer_name=data.get('designerName', ''),
            hsn_code=data.get('hsnCode', '998821'),
            items=calculated_items,
            total_qty=total_qty,
            total_value=total_value,
            avg_rate=round(avg_rate, 2),
            l_confirm_rate=0.00,
            h_confirm_rate=0.00,
            mistake_details=data.get('mistakeDetails', ''),
            reason=data.get('reason', ''),
            approval='Pending',
            status='Pending',
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Jobcard created successfully!',
            'jobcardNo': jobcard_no
        })
        
    except json.JSONDecodeError as e:
        return JsonResponse({
            'success': False,
            'message': f'Invalid JSON: {str(e)}'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST", "PUT", "PATCH"])
def edit_jobcard(request, pk):
    """Edit/Update existing jobcard - API Endpoint"""
    try:
        jobcard = get_object_or_404(JobCard, pk=pk)
        data = json.loads(request.body)
        
        # Process items
        items = data.get('items', [])
        calculated_items = []
        
        for item in items:
            width = float(item.get('width', 0) or 0)
            height = float(item.get('height', 0) or 0)
            rate = float(item.get('rate', 0) or 0)
            confirmed_amt = float(item.get('confirmedAmt', 0) or 0)
            qty = int(item.get('qty', 1) or 1)
            
            sq_inch = width * height
            amt = sq_inch * rate
            confirmed_rate = confirmed_amt / sq_inch if sq_inch != 0 else 0
            value = confirmed_amt * qty
            
            calculated_items.append({
                'particulars': item.get('particulars', ''),
                'width': width,
                'height': height,
                'rate': rate,
                'qty': qty,
                'sq_inch': round(sq_inch, 2),
                'amt': round(amt, 2),
                'confirmed_amt': round(confirmed_amt, 2),
                'confirmed_rate': round(confirmed_rate, 4),
                'value': round(value, 2),
            })
        
        # Calculate totals
        total_qty = sum(i['qty'] for i in calculated_items)
        total_value = sum(i['value'] for i in calculated_items)
        avg_rate = sum(i['rate'] for i in calculated_items) / len(calculated_items) if calculated_items else 0
        
        # Parse date
        date_str = data.get('date', '')
        try:
            if 'Z' in date_str:
                job_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            else:
                job_date = datetime.fromisoformat(date_str)
        except:
            job_date = jobcard.date
        
        # Update JobCard fields
        jobcard.order_by = data.get('orderBy', jobcard.order_by)
        jobcard.customer_name = data.get('customerName', jobcard.customer_name)
        jobcard.style_no = data.get('styleNo', jobcard.style_no)
        jobcard.job_created_by = data.get('jobCreatedBy', jobcard.job_created_by)
        jobcard.style_name = data.get('styleName', jobcard.style_name)
        jobcard.customer_po_no = data.get('customerPONo', jobcard.customer_po_no)
        jobcard.combo = data.get('combo', jobcard.combo)
        jobcard.job_type = data.get('jobType', jobcard.job_type)
        jobcard.fabric_type = data.get('fabricType', jobcard.fabric_type)
        jobcard.designer_name = data.get('designerName', jobcard.designer_name)
        jobcard.hsn_code = data.get('hsnCode', jobcard.hsn_code)
        jobcard.items = calculated_items
        jobcard.total_qty = total_qty
        jobcard.total_value = total_value
        jobcard.avg_rate = round(avg_rate, 2)
        jobcard.mistake_details = data.get('mistakeDetails', jobcard.mistake_details)
        jobcard.reason = data.get('reason', jobcard.reason)
        jobcard.date = job_date
        
        if 'approval' in data:
            jobcard.approval = data['approval']
        if 'status' in data:
            jobcard.status = data['status']
        
        jobcard.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Jobcard updated successfully!',
            'jobcardNo': jobcard.jobcard_no
        })
        
    except json.JSONDecodeError as e:
        return JsonResponse({
            'success': False,
            'message': f'Invalid JSON: {str(e)}'
        }, status=400)
    except JobCard.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Jobcard not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)







@csrf_exempt
@require_http_methods(["GET"])
def get_jobcard_process_details(request, jobcard_no):
    """Get jobcard details for process report"""
    try:
        jobcard = JobCard.objects.get(jobcard_no=jobcard_no)
        
        # Get items from JSON field
        items = jobcard.items or []
        
        # Prepare printing data from jobcard items
        printing_data = []
        for idx, item in enumerate(items, 1):
            qty = float(item.get('qty', 0))
            # Example: P.Qty is 95% of O.Qty (you can change this logic)
            p_qty = qty * 0.95
            
            printing_data.append({
                's_no': idx,
                'date': jobcard.date.strftime('%d-%m-%Y') if jobcard.date else '',
                'shift': 'Morning',  # You can add shift field in your model
                'machine_no': 'M001',  # You can add machine field
                'operator': jobcard.designer_name or 'N/A',
                'particulars': item.get('particulars', ''),
                'o_qty': qty,
                'p_qty': round(p_qty, 2),
            })
        
        # Prepare fusing data (currently empty - you can create Fusing model later)
        fusing_data = []
        # Example for future:
        # fusing_entries = Fusing.objects.filter(jobcard=jobcard)
        # for entry in fusing_entries:
        #     fusing_data.append({...})
        
        # Prepare delivery data (currently empty - you can create Delivery model later)
        delivery_data = []
        # Example for future:
        # delivery_entries = Delivery.objects.filter(jobcard=jobcard)
        # for entry in delivery_entries:
        #     delivery_data.append({...})
        
        return JsonResponse({
            'success': True,
            'data': {
                'customerName': jobcard.customer_name or '',
                'address': getattr(jobcard, 'customer_address', 'N/A'),  # Add if you have
                'quantity': float(jobcard.total_qty or 0),
                'printing': printing_data,
                'fusing': fusing_data,
                'delivery': delivery_data,
            }
        })
        
    except JobCard.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Jobcard not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)
    





    
@csrf_exempt
@require_http_methods(["GET"])
def get_summary(request):
    """Get jobcard summary statistics"""
    try:
        total_jobcards = JobCard.objects.count()
        pending_jobcards = JobCard.objects.filter(status='Pending').count()
        approved_jobcards = JobCard.objects.filter(status='Approved').count()
        rejected_jobcards = JobCard.objects.filter(status='Rejected').count()
        
        total_value = JobCard.objects.aggregate(
            total=Sum('total_value')
        )['total'] or 0
        
        now = datetime.now()
        this_month_jobcards = JobCard.objects.filter(
            created_at__year=now.year,
            created_at__month=now.month
        ).count()
        
        return JsonResponse({
            'success': True,
            'summary': {
                'totalJobcards': total_jobcards,
                'pendingJobcards': pending_jobcards,
                'approvedJobcards': approved_jobcards,
                'rejectedJobcards': rejected_jobcards,
                'totalValue': round(total_value, 2),
                'thisMonthJobcards': this_month_jobcards,
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def delete_jobcard(request, pk):
    """Delete jobcard - API Endpoint"""
    try:
        jobcard = JobCard.objects.get(id=pk)
        jobcard.delete()
        return JsonResponse({'success': True, 'message': 'Deleted successfully'})
    except JobCard.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Jobcard not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


# ============================================================================
# PARTY VIEWS
# ============================================================================

def party_list(request):
    qs = Party.objects.order_by("-created_at")
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(name__icontains=q)

    return render(request, "master/party_list.html", {"parties": qs, "q": q})

def party_create(request):
    if request.method == "POST":
        form = PartyForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.party_no = generate_doc_no("PTY", "PTY")
            obj.save()
            messages.success(request, "Party created successfully!")
            return redirect("party_list")
    else:
        form = PartyForm()

    return render(request, "master/party_form.html", {"form": form})


# ============================================================================
# QUOTATION VIEWS
# ============================================================================

def quotation_create(request):
    if request.method == "POST":
        form = QuotationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('quotation_list')
    else:
        form = QuotationForm()
    return render(request, 'jobcard/quotation_form.html', {'form': form})

def generate_quotation_no():
    today = timezone.now()
    yy = today.strftime("%y")
    mm = today.strftime("%m")
    prefix = f"JQ-{yy}{mm}-"

    last_quotation = Quotation.objects.filter(
        quotation_no__startswith=prefix
    ).order_by("-quotation_no").first()

    if last_quotation:
        last_serial = int(last_quotation.quotation_no.split("-")[-1])
        new_serial = last_serial + 1
    else:
        new_serial = 1

    return f"{prefix}{new_serial:03d}"

def quotation_form(request):
    quotation_no = generate_quotation_no()

    if request.method == "POST":
        form = QuotationForm(request.POST, request.FILES)

        if form.is_valid():
            quotation = form.save(commit=False)
            quotation.quotation_no = quotation_no
            quotation.created_by = request.user.username
            quotation.save()

            # ✅ GET LIST (important)
            particulars_list = request.POST.getlist("particulars[]")
            width_list = request.POST.getlist("width[]")
            height_list = request.POST.getlist("height[]")
            rate_list = request.POST.getlist("rate[]")
            confirmed_list = request.POST.getlist("confirmed_amt[]")
            qty_list = request.POST.getlist("qty[]")

            total_qty = 0
            total_value = 0

            for i in range(len(particulars_list)):

                if particulars_list[i]:  # skip empty row

                    width = float(width_list[i] or 0)
                    height = float(height_list[i] or 0)
                    rate = float(rate_list[i] or 0)
                    confirmed = float(confirmed_list[i] or 0)
                    qty = int(qty_list[i] or 0)

                    sq = width * height
                    amt = sq * rate
                    value = confirmed * qty

                    total_qty += qty
                    total_value += value

                    QuotationItem.objects.create(
                        quotation=quotation,
                        particulars=particulars_list[i],
                        width=width,
                        height=height,
                        rate=rate,
                        amt=amt,
                        confirmed_amt=confirmed,
                        qty=qty,
                        value=value,
                    )

            # ✅ Save totals in quotation table
            quotation.total_qty = total_qty
            quotation.total_value = total_value
            quotation.save()

            return redirect("quotation_list")

    else:
        form = QuotationForm()

    return render(request, "jobcard/quotation_form.html", {
        "form": form,
        "quotation_no": quotation_no
    })


def quotation_list(request):
    today = timezone.now().date()

    qno = request.GET.get("quotation_no")
    customer = request.GET.get("customer_name")
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")
    job_type = request.GET.get("job_type")
    fabric_type = request.GET.get("fabric_type")

    # Default: TODAY only
    quotations = Quotation.objects.filter(date__date=today).order_by("-id")

    # If any filter is used → show ALL
    if qno or customer or from_date or to_date or job_type or fabric_type:
        quotations = Quotation.objects.all().order_by("-id")

        if qno:
            quotations = quotations.filter(quotation_no__icontains=qno)

        if customer:
            quotations = quotations.filter(customer_name__icontains=customer)

        if job_type and job_type != "All":
            quotations = quotations.filter(job_type=job_type)

        if fabric_type and fabric_type != "All":
            quotations = quotations.filter(fabric_type=fabric_type)

        # Date filter
        if from_date and to_date:
            quotations = quotations.filter(date__date__range=[from_date, to_date])
        elif from_date:
            quotations = quotations.filter(date__date__gte=from_date)
        elif to_date:
            quotations = quotations.filter(date__date__lte=to_date)

    return render(request, "jobcard/quotation_list.html", {"quotations": quotations})

def quotation_view(request, pk):
    quotation = Quotation.objects.get(id=pk)
    return render(request, "jobcard/quotation_view.html", {"quotation": quotation})

def quotation_edit(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)

    if request.method == "POST":
        form = QuotationForm(request.POST, request.FILES, instance=quotation)
        if form.is_valid():
            form.save()
            return redirect("quotation_list")
    else:
        form = QuotationForm(instance=quotation)

    return render(request, "jobcard/quotation_form.html", {"form": form})

def quotation_delete(request, pk):
    quotation = Quotation.objects.get(id=pk)
    quotation.delete()
    return redirect("quotation_list")

def quotation_customer_report(request):
    today = timezone.now().date()

    from_date = request.GET.get("from_date", "")
    to_date = request.GET.get("to_date", "")
    customer_name = request.GET.get("customer_name", "")

    # Default: TODAY only
    quotations = Quotation.objects.prefetch_related("items").filter(date__date=today).order_by("-id")

    # If user uses search → show all data
    if from_date or to_date or customer_name:
        quotations = Quotation.objects.prefetch_related("items").all().order_by("-id")

        if from_date:
            quotations = quotations.filter(date__date__gte=from_date)

        if to_date:
            quotations = quotations.filter(date__date__lte=to_date)

        if customer_name:
            quotations = quotations.filter(customer_name__icontains=customer_name)

    report_data = []
    for quotation in quotations:
        for item in quotation.items.all():
            report_data.append({
                "date": quotation.date,
                "jobcard_no": quotation.quotation_no,
                "customer_name": quotation.customer_name,
                "particulars": item.particulars,
                "quantity": item.qty,
                "confirmed_rate": item.confirmed_amt,
                "amt": item.value,
            })

    return render(request, "jobcard/quotation_customer_report.html", {
        "report_data": report_data,
        "from_date": from_date,
        "to_date": to_date,
        "customer_name": customer_name,
    })


# ============================================================================
# OTHER PAGES
# ============================================================================

def company_creation(request):
    return render(request, 'mastercreation/company_creation.html')

def party_creation(request):
    return render(request, 'mastercreation/party_creation.html')

def user_type_creation(request):
    return render(request, 'mastercreation/user_type_creation.html')

def fusing(request):
    return render(request, 'fusing/fusing.html')

def printing(request):
    return render(request, 'printing/printing.html')

def consumable(request):
    return render(request, 'consumable/consumable.html')

def accounts(request):
    return render(request, 'accounts/accounts.html')

def delivery(request):
    return render(request, 'delivery/delivery.html')

def operator(request):
    return render(request, 'mastercreation/operator.html')

def measurement(request):
    return render(request, 'mastercreation/measurement.html')

def userpermission(request):
    return render(request, 'mastercreation/userpermission.html')

def userscreen(request):
    return render(request, 'mastercreation/userscreen.html')

def machinecreation(request):
    return render(request, 'mastercreation/machinecreation.html')

def shift(request):
    return render(request, 'mastercreation/shift.html')

def paymentterms(request):
    return render(request, 'mastercreation/paymentterms.html')

def consumablecreation(request):
    return render(request, 'mastercreation/consumablecreation.html')

def fabrictype(request):
    return render(request, 'mastercreation/fabrictype.html')

def rollsize(request):
    return render(request, 'mastercreation/rollsize.html')

def gapcreation(request):
    return render(request, 'mastercreation/gapcreation.html')

def jobtypecreation(request):
    return render(request, 'mastercreation/jobtypecreation.html')

def customerstatus(request):
    return render(request, 'mastercreation/customerstatus.html')

def user_name(request):
    return render(request, 'mastercreation/user_name.html')

def job_no_wise_report(request):
    return render(request, 'fusing/job-no-wise-report.html')

def fusing_operator_wise_report(request):
    return render(request, 'fusing/fusing-operator-wise-report.html')

def fusing_machine_wise_report(request):
    return render(request, 'fusing/fusing-machine-wise-report.html')

def date_wise_report(request):
    return render(request, 'fusing/date-wise-report.html')

def fusing_customer_wise_report(request):
    return render(request, 'fusing/fusing-customer-wise-report.html')

def fusing_production_entry(request):
    return render(request, 'fusing/fusing-production-entry.html')

def printer_customer(request):
    return render(request, 'printing/printer_customer.html')

def printer_data(request):
    return render(request, 'printing/printer_data.html')

def printer_jobwise(request):
    return render(request, 'printing/printer_jobwise.html')

def printer_machine(request):
    return render(request, 'printing/printer_machine.html')

def printer_operator(request):
    return render(request, 'printing/printer_operator.html')

def printer_production(request):
    return render(request, 'printing/printer_production.html')

def ink_entry(request):
    return render(request, 'consumable/ink_entry.html')

def return_form(request):
    return render(request, 'consumable/return_form.html')

def stock_report(request):
    return render(request, 'consumable/stock_report.html')

def inward(request):
    return render(request, 'delivery/inward.html')

def fabric(request):
    return render(request, 'delivery/fabric.html')

def returned(request):
    return render(request, 'delivery/return.html')

def sticker(request):
    return render(request, 'delivery/sticker.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")