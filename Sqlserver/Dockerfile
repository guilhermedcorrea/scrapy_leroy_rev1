FROM mcr.microsoft.com/mssql/server:2019-latest

ENV SA_PASSWORD=Mudar@123
ENV ACCEPT_EULA=Y

COPY tabelas/setup.sql /docker-entrypoint-initdb.d/

CMD ["/opt/mssql/bin/sqlservr"]