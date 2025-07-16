FROM apache/airflow:2.8.2-python3.10

USER root

# Variables de version
ENV SPARK_VERSION=3.5.1 \
    HADOOP_VERSION=3 \
    JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# Installer Java, wget, et Spark
RUN apt-get update && \
    apt-get install -y openjdk-17-jre-headless wget curl gnupg2 && \
    wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar -xzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz -C /opt/ && \
    mv /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark && \
    rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# Définir les variables d'environnement pour Spark
ENV SPARK_HOME=/opt/spark
ENV PATH="$SPARK_HOME/bin:$PATH"

# Revenir à l'utilisateur airflow
USER airflow

# Installer les bibliothèques Python nécessaires
RUN pip install psycopg2-binary dbt-postgres

# Installer dbt (version compatible avec ton environnement Python)
RUN pip install dbt-postgres



