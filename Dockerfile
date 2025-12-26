FROM public.ecr.aws/lambda/python:3.12

# Install dependencies
COPY lambda_requirements.txt ${LAMBDA_TASK_ROOT}/
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/lambda_requirements.txt

# Copy function code
COPY lambda_handler.py ${LAMBDA_TASK_ROOT}/
COPY src/ ${LAMBDA_TASK_ROOT}/src/

# Set the CMD to your handler
CMD ["lambda_handler.lambda_handler"]
