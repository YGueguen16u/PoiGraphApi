### This is a testing script to ensure snowflake connection is valid
from utils.getSecrets import _get_secret
import snowflake.connector

# Gets the version
ctx = snowflake.connector.connect(
    user=_get_secret("snowflake_user"),
    password=_get_secret("snowflake_secret"),
    account=_get_secret("snowflake_account")
    )
cs = ctx.cursor()
try:
    cs.execute("SELECT current_version()")
    one_row = cs.fetchone()
    print(one_row[0])
finally:
    cs.close()
ctx.close()