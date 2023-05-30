import logging
import psycopg2
import os
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    time = req.params.get('time')
    if not time:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            time = req_body.get('time')

    if time:
        conn = psycopg2.connect(database=os.environ['PG_DATABASE'], user=os.environ['PG_USERNAME'], password=os.environ['PG_PASSWORD'], 
                                host=os.environ['PG_HOST'], port=os.environ['PG_PORT'])
    
        cursor = conn.cursor()

        cursor.callproc('delete_old_rows', [int(time)])
        deleted_rows = cursor.fetchone()[0]

        # Commit the changes to the database
        conn.commit()
        conn.close()

        # Return the number of rows deleted
        return func.HttpResponse(f"{deleted_rows} rows have been deleted. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a time in the query string or in the request body for rows to be deleted.",
             status_code=200
        )