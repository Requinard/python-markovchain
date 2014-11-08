import markov

if __name__ == '__main__':
    brain = markov.Brain()

    try:
        brain.load()
    except:
        brain.learn(
            'hi my name is Al and i live in a box that i like very much and i can live in there as long as i want')
        brain.learn(
            "The problem is motivation. You wanna learn something? But the fact is you are in prison. Yeah you can learn about rocket science and become a master in it but no one gonna give you a job since you have a record. I am not saying you shouldn't learn but to develop that focus when you are in prison probably the hardest thing someone can do. Just my opinion, I think the motivation is very important.")
        brain.learn(
            "Served 30 months in Florida at age 18...food was terrible, boredom is mind numbing, the feeling that the world is leaving you behind is quite painful...perhaps the worst of it though is the stigma associated with being a convicted felon. I have been turned down twice for jobs I am capable of excelling at (former space coast area Machinist now living in oil country). Problem is, I am totally honest with them and the convictions are 25 years old.")

        brain.learn(
            "Served 30 months in Florida at age 18...food was terrible, boredom is mind numbing, the feeling that the world is leaving you behind is quite painful...perhaps the worst of it though is the stigma associated with being a convicted felon. I have been turned down twice for jobs I am capable of excelling at (former space coast area Machinist now living in oil country). Problem is, I am totally honest with them and the convictions are 25 years old.")

    print brain.respond("Prison terms need to at least consider why a person did something. It's so fucked that his uncle killed those people drunk driving, but he obviously didn't intend to.")