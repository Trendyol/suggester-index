FROM python
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

ENV DOC_TYPE = ""
ENV TARGET_ES_URL = ""
ENV SOURCE_ES_URL = ""
ENV SOURCE_INDEX = ""
ENV TARGET_INDEX = ""
ENV SOURCE_ATTRIBUTE = ""

CMD python -u ./generateFuzzyKeywords.py