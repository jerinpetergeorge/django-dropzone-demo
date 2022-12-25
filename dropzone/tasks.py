from dropzone.models import Session


def merge_chunks_async(session_id: int, **kwargs):
    merge_chunks(session_id=session_id, **kwargs)


def merge_chunks(session_id: int, **kwargs):
    session: Session = Session.objects.get(id=session_id)
    session.merge_chunks(**kwargs)
