This project serves a purely educational purpose and is built upon an existing project developed by the team of Max Pumperla and Kevin Ferguson (https://github.com/maxpumperla/deep_learning_and_the_game_of_go/tree/master). Please refer their Github repository or the corresponding book "Deep Learning and the Game of Go" for more detailed information. The modifications I have made are as follows:

1. The data decoding section has been restructured to 9 times 9 board size, the used dataset is collected from an App, Go Quest (https://www.dropbox.com/s/abpzmqrw7gyvlzt/go9.tgz).

2. Addressed the issue of non-functional code arising from changes in the core Python modules.

3. Corrected the implementation of MCTS in AG and the scoring rule.

4. Completed the iteration of AG and AGZ.

5. Created a new agent AG-AGZ that combines the characters of AlphaGo and AlphaGo Zero.

6. Integrated shell codes to facilitate the parallel execution of these modules on Baobab.

7. This code has been successfully run on Pyhton3.9 and Python3.8 with GCC/10.2.0, CUDA/11.1.1 OpenMPI/4.0.5, Python/3.8.6, TensorFlow/2.4.1.