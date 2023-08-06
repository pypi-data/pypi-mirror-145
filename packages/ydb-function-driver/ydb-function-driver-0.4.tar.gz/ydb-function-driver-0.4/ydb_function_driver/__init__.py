import os
import ydb

YDB_ENDPOINT = os.environ["YDB_ENDPOINT"]
YDB_DATABASE = os.environ["YDB_DATABASE"]

driver = ydb.Driver(endpoint=YDB_ENDPOINT, database=YDB_DATABASE)
driver.wait(fail_fast=True, timeout=5)
pool = ydb.SessionPool(driver)


def execute_query(query):
  def set_it(session):
    return session.transaction().execute(
        query,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    )
  result = pool.retry_operation_sync(set_it)
  if result and len(result) and result[0].rows:
    return list(result[0].rows)  
  return result

