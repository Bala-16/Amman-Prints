from django.db import transaction
from django.utils import timezone
from .models import DocSequence

def generate_doc_no(doc_type: str, prefix: str) -> str:
    """
    Example:
    doc_type='JC', prefix='JC' -> JC-2602-0001
    """
    yymm = timezone.now().strftime("%y%m")

    with transaction.atomic():
        seq, _ = DocSequence.objects.select_for_update().get_or_create(
            doc_type=doc_type, yymm=yymm, defaults={"last_no": 0}
        )
        seq.last_no += 1
        seq.save()

        return f"{prefix}-{yymm}-{seq.last_no:04d}"
