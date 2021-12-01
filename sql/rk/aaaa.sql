create or replace procedure table_index(table_form character)
language 'plpgsql'
as $$ 
declare
	rec record;
begin
for rec in (
	select tablename, indexdef
	from pg_indexes
	where tablename = table_form) loop
	raise notice '% %', rec.tablename, rec.indexdef;
	end loop;
end; $$;

call table_index('users');