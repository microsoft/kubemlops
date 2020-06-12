FROM gcr.io/kubeflow-images-public/tensorflow-2.1.0-notebook-cpu:1.0.0
USER root
RUN pip install pandas
RUN pip install seaborn
RUN pip install scikit-learn
# Install Kale python package globally
RUN pip install kubeflow-kale
# Install Kale JupyterLab extension
RUN jupyter labextension install kubeflow-kale-launcher

RUN echo "jovyan ALL=(ALL:ALL) NOPASSWD:ALL" > /etc/sudoers.d/jovyan
WORKDIR /home/jovyan
USER jovyan

ENV NB_PREFIX /
CMD ["sh","-c", "jupyter lab --notebook-dir=/home/jovyan --ip=0.0.0.0 --no-browser --allow-root --port=8888 --NotebookApp.token='' --NotebookApp.password='' --NotebookApp.allow_origin='*' --NotebookApp.base_url=${NB_PREFIX}"]


