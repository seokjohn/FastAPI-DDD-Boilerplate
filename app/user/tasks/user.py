from core.db import SyncSessionContext



def test_schedule():
    with SyncSessionContext() as session:
        query = (
            # 레포 및 쿼리 추가
            ...
        )
        session.execute(query)
        session.commit()
