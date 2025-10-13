LearnPro

Our RAG agent retrieves the answers for a query from the provided learning material based on the progress of the student. It uses [Pathway](https://pathway.com/) and the document-based question-answering system is supported by Gemini. The frontend is achieved using gradio.

Architecture of the pipeline
![Architecture](<The data is loaded from the files loaded in Q5 folder in data..png>)

You can ask a query from the given data source and you will get a context specific and relevant response generated from the data provided.
Suppose you have a want to ask a doubt on electomagnetism.

RAG Query Input
![RAG Query Input](<rag query input.png>)

RAG Query Output
![RAG Query Output](<rag query output.png>)

There is another feature that allows the user to update the mastery(progress) of a student after a quiz. 
Suppose the student gave incorrect answers in the quiz.

Mastery Update Input
![Mastery is 0.6](<mastery update input.png>)

Mastery Update Output
![Mastery is reduced to 0.55](<mastery update output.png>)

Steps to run the program
1. Open a cmd terminal and keep docker engine running behind. Build a docker image in the directory of the project with the name my-pathway-app. The command is
docker build -t my-pathway-app . 
2. Run a container and mount it on /app and the data folder stored in /app. For example, docker run -it --rm -v %cd%:/app -v %cd%\data:/app/data -p 8008:8000 my-pathway-app.
3. Install gradio and requests from pip to run the frontend.
3. Open another cmd terminal and enter the directory where the project folder exists.
4. Give the command python frontend.py and type http://localhost:7860 on your web browser to access it.
