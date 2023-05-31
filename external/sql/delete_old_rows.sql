CREATE OR REPLACE FUNCTION delete_old_rows(current_time_unix INTEGER)
      RETURNS INTEGER AS $dist$
        DECLARE
          deletion_date INTEGER;
          deleted_rows INTEGER := 0;
          seven_days INTEGER := 604800;
        BEGIN
          -- Calculate the deletion date (7 days ago from the current time parameter)
          deletion_date := current_time_unix - seven_days;

          -- Delete rows where the time column is older than the deletion date
          DELETE FROM flight
          WHERE lastseen < deletion_date;
          
          GET DIAGNOSTICS deleted_rows = ROW_COUNT;

          RETURN deleted_rows;
        END;
      $dist$ LANGUAGE plpgsql;