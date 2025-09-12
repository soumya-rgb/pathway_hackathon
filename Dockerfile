FROM pathwaycom/pathway:latest

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglx-mesa0 \
    libglib2.0-0t64 \
    python3-opencv \
    tesseract-ocr-eng \
 && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "python", "./main.py" ]

# docker run -it -v $(pwd):/app my-pathway-app
# docker run -it -v $(pwd):/app -p 8008:8000 my-pathway-app sh

# docker run -it -v ${PWD}:/app -p 8008:8000 my-pathway-app sh


# docker build -t my-pathway-app .

# docker run -it --rm -v ${PWD}:/app -p 8008:8000 my-pathway-app


