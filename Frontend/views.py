# from django.shortcuts import render, get_object_or_404
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_http_methods
# from django.db.models import Sum  # ✅ இதை சேர்க்கவும்
# from .models import JobCard
# import json
# from datetime import datetime

# def jobcard_form_view(request):
#     """Render the jobcard form page"""
#     return render(request, 'jobcard/jobcard_form.html')

# @csrf_exempt
# @require_http_methods(["GET"])
# def get_jobcards(request):
#     """Get all jobcards"""
#     try:
#         jobcards = JobCard.objects.all().order_by('-created_at')
#         data = []
#         for jc in jobcards:
#             data.append({
#                 'id': jc.id,
#                 'jobcardNo': jc.jobcard_no,
#                 'date': jc.date.isoformat() if jc.date else '',
#                 'customerName': jc.customer_name,
#                 'jobCreatedBy': jc.job_created_by,
#                 'jobType': jc.job_type,
#                 'fabricType': jc.fabric_type,
#                 'totalQty': jc.total_qty,
#                 'totalValue': jc.total_value,
#                 'avgRate': jc.avg_rate,
#                 'lConfirmRate': jc.l_confirm_rate,
#                 'hConfirmRate': jc.h_confirm_rate,
#                 'approval': jc.approval,
#                 'status': jc.status,
#             })
#         return JsonResponse({'jobcards': data})
#     except Exception as e:
#         return JsonResponse({'success': False, 'message': str(e)}, status=500)

# @csrf_exempt
# @require_http_methods(["POST"])
# def create_jobcard(request):
#     """Create new jobcard"""
#     try:
#         data = json.loads(request.body)
        
#         # Generate Jobcard Number
#         now = datetime.now()
#         year = now.strftime('%y')
#         month = now.strftime('%m')
        
#         last_jobcard = JobCard.objects.filter(
#             jobcard_no__startswith=f'JC-{year}{month}-'
#         ).order_by('-jobcard_no').first()
        
#         if last_jobcard:
#             last_seq = int(last_jobcard.jobcard_no.split('-')[2])
#             sequence = str(last_seq + 1).zfill(4)
#         else:
#             sequence = '0001'
        
#         jobcard_no = f'JC-{year}{month}-{sequence}'
        
#         # Process items
#         items = data.get('items', [])
#         calculated_items = []
        
#         for item in items:
#             width = float(item.get('width', 0) or 0)
#             height = float(item.get('height', 0) or 0)
#             rate = float(item.get('rate', 0) or 0)
#             confirmed_amt = float(item.get('confirmedAmt', 0) or 0)
#             qty = int(item.get('qty', 1) or 1)
            
#             sq_inch = width * height
#             amt = sq_inch * rate
#             confirmed_rate = confirmed_amt / sq_inch if sq_inch != 0 else 0
#             value = confirmed_amt * qty
            
#             calculated_items.append({
#                 'particulars': item.get('particulars', ''),
#                 'width': width,
#                 'height': height,
#                 'rate': rate,
#                 'qty': qty,
#                 'sq_inch': round(sq_inch, 2),
#                 'amt': round(amt, 2),
#                 'confirmed_amt': round(confirmed_amt, 2),
#                 'confirmed_rate': round(confirmed_rate, 4),
#                 'value': round(value, 2),
#             })
        
#         # Calculate totals
#         total_qty = sum(i['qty'] for i in calculated_items)
#         total_value = sum(i['value'] for i in calculated_items)
#         avg_rate = sum(i['rate'] for i in calculated_items) / len(calculated_items) if calculated_items else 0
        
#         # Parse date
#         date_str = data.get('date', '')
#         try:
#             if 'Z' in date_str:
#                 job_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
#             else:
#                 job_date = datetime.fromisoformat(date_str)
#         except:
#             job_date = datetime.now()
        
#         # Create JobCard
#         jobcard = JobCard.objects.create(
#             jobcard_no=jobcard_no,
#             date=job_date,
#             order_by=data.get('orderBy', ''),
#             customer_name=data.get('customerName', ''),
#             style_no=data.get('styleNo', ''),
#             job_created_by=data.get('jobCreatedBy', 'admin'),
#             style_name=data.get('styleName', ''),
#             customer_po_no=data.get('customerPONo', ''),
#             combo=data.get('combo', ''),
#             job_type=data.get('jobType', ''),
#             fabric_type=data.get('fabricType', ''),
#             designer_name=data.get('designerName', ''),
#             hsn_code=data.get('hsnCode', '998821'),
#             items=calculated_items,
#             total_qty=total_qty,
#             total_value=total_value,
#             avg_rate=round(avg_rate, 2),
#             l_confirm_rate=0.00,
#             h_confirm_rate=0.00,
#             mistake_details=data.get('mistakeDetails', ''),
#             reason=data.get('reason', ''),
#             approval='Pending',
#             status='Pending',
#         )
        
#         return JsonResponse({
#             'success': True,
#             'message': 'Jobcard created successfully!',
#             'jobcardNo': jobcard_no
#         })
        
#     except json.JSONDecodeError as e:
#         return JsonResponse({
#             'success': False,
#             'message': f'Invalid JSON: {str(e)}'
#         }, status=400)
#     except Exception as e:
#         return JsonResponse({
#             'success': False,
#             'message': f'Error: {str(e)}'
#         }, status=500)

# @csrf_exempt
# @require_http_methods(["POST", "PUT", "PATCH"])
# def edit_jobcard(request, pk):
#     """Edit/Update existing jobcard"""
#     try:
#         jobcard = get_object_or_404(JobCard, pk=pk)
#         data = json.loads(request.body)
        
#         # Process items
#         items = data.get('items', [])
#         calculated_items = []
        
#         for item in items:
#             width = float(item.get('width', 0) or 0)
#             height = float(item.get('height', 0) or 0)
#             rate = float(item.get('rate', 0) or 0)
#             confirmed_amt = float(item.get('confirmedAmt', 0) or 0)
#             qty = int(item.get('qty', 1) or 1)
            
#             sq_inch = width * height
#             amt = sq_inch * rate
#             confirmed_rate = confirmed_amt / sq_inch if sq_inch != 0 else 0
#             value = confirmed_amt * qty
            
#             calculated_items.append({
#                 'particulars': item.get('particulars', ''),
#                 'width': width,
#                 'height': height,
#                 'rate': rate,
#                 'qty': qty,
#                 'sq_inch': round(sq_inch, 2),
#                 'amt': round(amt, 2),
#                 'confirmed_amt': round(confirmed_amt, 2),
#                 'confirmed_rate': round(confirmed_rate, 4),
#                 'value': round(value, 2),
#             })
        
#         # Calculate totals
#         total_qty = sum(i['qty'] for i in calculated_items)
#         total_value = sum(i['value'] for i in calculated_items)
#         avg_rate = sum(i['rate'] for i in calculated_items) / len(calculated_items) if calculated_items else 0
        
#         # Parse date
#         date_str = data.get('date', '')
#         try:
#             if 'Z' in date_str:
#                 job_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
#             else:
#                 job_date = datetime.fromisoformat(date_str)
#         except:
#             job_date = jobcard.date
        
#         # Update JobCard fields
#         jobcard.order_by = data.get('orderBy', jobcard.order_by)
#         jobcard.customer_name = data.get('customerName', jobcard.customer_name)
#         jobcard.style_no = data.get('styleNo', jobcard.style_no)
#         jobcard.job_created_by = data.get('jobCreatedBy', jobcard.job_created_by)
#         jobcard.style_name = data.get('styleName', jobcard.style_name)
#         jobcard.customer_po_no = data.get('customerPONo', jobcard.customer_po_no)
#         jobcard.combo = data.get('combo', jobcard.combo)
#         jobcard.job_type = data.get('jobType', jobcard.job_type)
#         jobcard.fabric_type = data.get('fabricType', jobcard.fabric_type)
#         jobcard.designer_name = data.get('designerName', jobcard.designer_name)
#         jobcard.hsn_code = data.get('hsnCode', jobcard.hsn_code)
#         jobcard.items = calculated_items
#         jobcard.total_qty = total_qty
#         jobcard.total_value = total_value
#         jobcard.avg_rate = round(avg_rate, 2)
#         jobcard.mistake_details = data.get('mistakeDetails', jobcard.mistake_details)
#         jobcard.reason = data.get('reason', jobcard.reason)
#         jobcard.date = job_date
        
#         if 'approval' in data:
#             jobcard.approval = data['approval']
#         if 'status' in data:
#             jobcard.status = data['status']
        
#         jobcard.save()
        
#         return JsonResponse({
#             'success': True,
#             'message': 'Jobcard updated successfully!',
#             'jobcardNo': jobcard.jobcard_no
#         })
        
#     except json.JSONDecodeError as e:
#         return JsonResponse({
#             'success': False,
#             'message': f'Invalid JSON: {str(e)}'
#         }, status=400)
#     except JobCard.DoesNotExist:
#         return JsonResponse({
#             'success': False,
#             'message': 'Jobcard not found'
#         }, status=404)
#     except Exception as e:
#         return JsonResponse({
#             'success': False,
#             'message': f'Error: {str(e)}'
#         }, status=500)

# @csrf_exempt
# @require_http_methods(["GET"])
# def get_summary(request):
#     """Get jobcard summary statistics"""
#     try:
#         total_jobcards = JobCard.objects.count()
#         pending_jobcards = JobCard.objects.filter(status='Pending').count()
#         approved_jobcards = JobCard.objects.filter(status='Approved').count()
#         rejected_jobcards = JobCard.objects.filter(status='Rejected').count()
        
#         total_value = JobCard.objects.aggregate(
#             total=Sum('total_value')
#         )['total'] or 0
        
#         now = datetime.now()
#         this_month_jobcards = JobCard.objects.filter(
#             created_at__year=now.year,
#             created_at__month=now.month
#         ).count()
        
#         return JsonResponse({
#             'success': True,
#             'summary': {
#                 'totalJobcards': total_jobcards,
#                 'pendingJobcards': pending_jobcards,
#                 'approvedJobcards': approved_jobcards,
#                 'rejectedJobcards': rejected_jobcards,
#                 'totalValue': round(total_value, 2),
#                 'thisMonthJobcards': this_month_jobcards,
#             }
#         })
#     except Exception as e:
#         return JsonResponse({
#             'success': False,
#             'message': str(e)
#         }, status=500)

# @csrf_exempt
# @require_http_methods(["POST"])
# def delete_jobcard(request, pk):
#     """Delete jobcard"""
#     try:
#         jobcard = JobCard.objects.get(id=pk)
#         jobcard.delete()
#         return JsonResponse({'success': True, 'message': 'Deleted successfully'})
#     except JobCard.DoesNotExist:
#         return JsonResponse({'success': False, 'message': 'Jobcard not found'}, status=404)
#     except Exception as e:
#         return JsonResponse({'success': False, 'message': str(e)}, status=500)from django.shortcuts import render, get_object_or_404
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_http_methods
# from django.db.models import Sum  # ✅ இதை சேர்க்கவும்
# from .models import JobCard
# import json
# from datetime import datetime

# def jobcard_form_view(request):
#     """Render the jobcard form page"""
#     return render(request, 'jobcard/jobcard_form.html')

# @csrf_exempt
# @require_http_methods(["GET"])
# def get_jobcards(request):
#     """Get all jobcards"""
#     try:
#         jobcards = JobCard.objects.all().order_by('-created_at')
#         data = []
#         for jc in jobcards:
#             data.append({
#                 'id': jc.id,
#                 'jobcardNo': jc.jobcard_no,
#                 'date': jc.date.isoformat() if jc.date else '',
#                 'customerName': jc.customer_name,
#                 'jobCreatedBy': jc.job_created_by,
#                 'jobType': jc.job_type,
#                 'fabricType': jc.fabric_type,
#                 'totalQty': jc.total_qty,
#                 'totalValue': jc.total_value,
#                 'avgRate': jc.avg_rate,
#                 'lConfirmRate': jc.l_confirm_rate,
#                 'hConfirmRate': jc.h_confirm_rate,
#                 'approval': jc.approval,
#                 'status': jc.status,
#             })
#         return JsonResponse({'jobcards': data})
#     except Exception as e:
#         return JsonResponse({'success': False, 'message': str(e)}, status=500)

# @csrf_exempt
# @require_http_methods(["POST"])
# def create_jobcard(request):
#     """Create new jobcard"""
#     try:
#         data = json.loads(request.body)
        
#         # Generate Jobcard Number
#         now = datetime.now()
#         year = now.strftime('%y')
#         month = now.strftime('%m')
        
#         last_jobcard = JobCard.objects.filter(
#             jobcard_no__startswith=f'JC-{year}{month}-'
#         ).order_by('-jobcard_no').first()
        
#         if last_jobcard:
#             last_seq = int(last_jobcard.jobcard_no.split('-')[2])
#             sequence = str(last_seq + 1).zfill(4)
#         else:
#             sequence = '0001'
        
#         jobcard_no = f'JC-{year}{month}-{sequence}'
        
#         # Process items
#         items = data.get('items', [])
#         calculated_items = []
        
#         for item in items:
#             width = float(item.get('width', 0) or 0)
#             height = float(item.get('height', 0) or 0)
#             rate = float(item.get('rate', 0) or 0)
#             confirmed_amt = float(item.get('confirmedAmt', 0) or 0)
#             qty = int(item.get('qty', 1) or 1)
            
#             sq_inch = width * height
#             amt = sq_inch * rate
#             confirmed_rate = confirmed_amt / sq_inch if sq_inch != 0 else 0
#             value = confirmed_amt * qty
            
#             calculated_items.append({
#                 'particulars': item.get('particulars', ''),
#                 'width': width,
#                 'height': height,
#                 'rate': rate,
#                 'qty': qty,
#                 'sq_inch': round(sq_inch, 2),
#                 'amt': round(amt, 2),
#                 'confirmed_amt': round(confirmed_amt, 2),
#                 'confirmed_rate': round(confirmed_rate, 4),
#                 'value': round(value, 2),
#             })
        
#         # Calculate totals
#         total_qty = sum(i['qty'] for i in calculated_items)
#         total_value = sum(i['value'] for i in calculated_items)
#         avg_rate = sum(i['rate'] for i in calculated_items) / len(calculated_items) if calculated_items else 0
        
#         # Parse date
#         date_str = data.get('date', '')
#         try:
#             if 'Z' in date_str:
#                 job_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
#             else:
#                 job_date = datetime.fromisoformat(date_str)
#         except:
#             job_date = datetime.now()
        
#         # Create JobCard
#         jobcard = JobCard.objects.create(
#             jobcard_no=jobcard_no,
#             date=job_date,
#             order_by=data.get('orderBy', ''),
#             customer_name=data.get('customerName', ''),
#             style_no=data.get('styleNo', ''),
#             job_created_by=data.get('jobCreatedBy', 'admin'),
#             style_name=data.get('styleName', ''),
#             customer_po_no=data.get('customerPONo', ''),
#             combo=data.get('combo', ''),
#             job_type=data.get('jobType', ''),
#             fabric_type=data.get('fabricType', ''),
#             designer_name=data.get('designerName', ''),
#             hsn_code=data.get('hsnCode', '998821'),
#             items=calculated_items,
#             total_qty=total_qty,
#             total_value=total_value,
#             avg_rate=round(avg_rate, 2),
#             l_confirm_rate=0.00,
#             h_confirm_rate=0.00,
#             mistake_details=data.get('mistakeDetails', ''),
#             reason=data.get('reason', ''),
#             approval='Pending',
#             status='Pending',
#         )
        
#         return JsonResponse({
#             'success': True,
#             'message': 'Jobcard created successfully!',
#             'jobcardNo': jobcard_no
#         })
        
#     except json.JSONDecodeError as e:
#         return JsonResponse({
#             'success': False,
#             'message': f'Invalid JSON: {str(e)}'
#         }, status=400)
#     except Exception as e:
#         return JsonResponse({
#             'success': False,
#             'message': f'Error: {str(e)}'
#         }, status=500)

# @csrf_exempt
# @require_http_methods(["POST", "PUT", "PATCH"])
# def edit_jobcard(request, pk):
#     """Edit/Update existing jobcard"""
#     try:
#         jobcard = get_object_or_404(JobCard, pk=pk)
#         data = json.loads(request.body)
        
#         # Process items
#         items = data.get('items', [])
#         calculated_items = []
        
#         for item in items:
#             width = float(item.get('width', 0) or 0)
#             height = float(item.get('height', 0) or 0)
#             rate = float(item.get('rate', 0) or 0)
#             confirmed_amt = float(item.get('confirmedAmt', 0) or 0)
#             qty = int(item.get('qty', 1) or 1)
            
#             sq_inch = width * height
#             amt = sq_inch * rate
#             confirmed_rate = confirmed_amt / sq_inch if sq_inch != 0 else 0
#             value = confirmed_amt * qty
            
#             calculated_items.append({
#                 'particulars': item.get('particulars', ''),
#                 'width': width,
#                 'height': height,
#                 'rate': rate,
#                 'qty': qty,
#                 'sq_inch': round(sq_inch, 2),
#                 'amt': round(amt, 2),
#                 'confirmed_amt': round(confirmed_amt, 2),
#                 'confirmed_rate': round(confirmed_rate, 4),
#                 'value': round(value, 2),
#             })
        
#         # Calculate totals
#         total_qty = sum(i['qty'] for i in calculated_items)
#         total_value = sum(i['value'] for i in calculated_items)
#         avg_rate = sum(i['rate'] for i in calculated_items) / len(calculated_items) if calculated_items else 0
        
#         # Parse date
#         date_str = data.get('date', '')
#         try:
#             if 'Z' in date_str:
#                 job_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
#             else:
#                 job_date = datetime.fromisoformat(date_str)
#         except:
#             job_date = jobcard.date
        
#         # Update JobCard fields
#         jobcard.order_by = data.get('orderBy', jobcard.order_by)
#         jobcard.customer_name = data.get('customerName', jobcard.customer_name)
#         jobcard.style_no = data.get('styleNo', jobcard.style_no)
#         jobcard.job_created_by = data.get('jobCreatedBy', jobcard.job_created_by)
#         jobcard.style_name = data.get('styleName', jobcard.style_name)
#         jobcard.customer_po_no = data.get('customerPONo', jobcard.customer_po_no)
#         jobcard.combo = data.get('combo', jobcard.combo)
#         jobcard.job_type = data.get('jobType', jobcard.job_type)
#         jobcard.fabric_type = data.get('fabricType', jobcard.fabric_type)
#         jobcard.designer_name = data.get('designerName', jobcard.designer_name)
#         jobcard.hsn_code = data.get('hsnCode', jobcard.hsn_code)
#         jobcard.items = calculated_items
#         jobcard.total_qty = total_qty
#         jobcard.total_value = total_value
#         jobcard.avg_rate = round(avg_rate, 2)
#         jobcard.mistake_details = data.get('mistakeDetails', jobcard.mistake_details)
#         jobcard.reason = data.get('reason', jobcard.reason)
#         jobcard.date = job_date
        
#         if 'approval' in data:
#             jobcard.approval = data['approval']
#         if 'status' in data:
#             jobcard.status = data['status']
        
#         jobcard.save()
        
#         return JsonResponse({
#             'success': True,
#             'message': 'Jobcard updated successfully!',
#             'jobcardNo': jobcard.jobcard_no
#         })
        
#     except json.JSONDecodeError as e:
#         return JsonResponse({
#             'success': False,
#             'message': f'Invalid JSON: {str(e)}'
#         }, status=400)
#     except JobCard.DoesNotExist:
#         return JsonResponse({
#             'success': False,
#             'message': 'Jobcard not found'
#         }, status=404)
#     except Exception as e:
#         return JsonResponse({
#             'success': False,
#             'message': f'Error: {str(e)}'
#         }, status=500)

# @csrf_exempt
# @require_http_methods(["GET"])
# def get_summary(request):
#     """Get jobcard summary statistics"""
#     try:
#         total_jobcards = JobCard.objects.count()
#         pending_jobcards = JobCard.objects.filter(status='Pending').count()
#         approved_jobcards = JobCard.objects.filter(status='Approved').count()
#         rejected_jobcards = JobCard.objects.filter(status='Rejected').count()
        
#         total_value = JobCard.objects.aggregate(
#             total=Sum('total_value')
#         )['total'] or 0
        
#         now = datetime.now()
#         this_month_jobcards = JobCard.objects.filter(
#             created_at__year=now.year,
#             created_at__month=now.month
#         ).count()
        
#         return JsonResponse({
#             'success': True,
#             'summary': {
#                 'totalJobcards': total_jobcards,
#                 'pendingJobcards': pending_jobcards,
#                 'approvedJobcards': approved_jobcards,
#                 'rejectedJobcards': rejected_jobcards,
#                 'totalValue': round(total_value, 2),
#                 'thisMonthJobcards': this_month_jobcards,
#             }
#         })
#     except Exception as e:
#         return JsonResponse({
#             'success': False,
#             'message': str(e)
#         }, status=500)

# @csrf_exempt
# @require_http_methods(["POST"])
# def delete_jobcard(request, pk):
#     """Delete jobcard"""
#     try:
#         jobcard = JobCard.objects.get(id=pk)
#         jobcard.delete()
#         return JsonResponse({'success': True, 'message': 'Deleted successfully'})
#     except JobCard.DoesNotExist:
#         return JsonResponse({'success': False, 'message': 'Jobcard not found'}, status=404)
#     except Exception as e:
#         return JsonResponse({'success': False, 'message': str(e)}, status=500)