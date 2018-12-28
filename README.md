# all-persons-fictitious

In the project all-persons-fictitious, we’re trying to see what it would look like to have conversations with entities that respond in music. In our installation, you experience communicating with an artificial intelligence, that rather than reply in conventional words, responds in sound that you can hear. As you keep talking, you will hear the music change over time. 

The way it works
  1.	You write something you want to tell the chatbot
  2.	The chatbot takes that input and thinks of a response
  3.	The chatbot’s response is analyzed for sentiment, that is its emotional and affective content
  4.	This information is sent to our synthesizer, which processes the emotional data into music

In doing this, we are building on the work of several different disciplines. Primarily, we rely on the development of chatbots within artificial intelligence, sentiment analysis within natural language processing, sonification of data, as well the open source movement around the digital audio workstation Pure Data. 


How to use it

Use Pute Data (https://puredata.info/) to run the .pd file. The chatbot and synth communicate via Open Sound Control (OSC). To use OSC in pd, you need to download the mrpeach library (Do this via "Help" > "Find externals" and search for "mrpeach"). To activate sound in pd, remember to turn on DSP ("Media" > "DSP On").
