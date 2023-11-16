# Definitions

## [Big O Notation](https://en.wikipedia.org/wiki/Big_O_notation)

In mathematics, big O notation describes the limiting behavior of a function when the argument tends towards a particular value or infinity, usually in terms of simpler functions. It is a member of a family of notations invented by Paul Bachmann, Edmund Landau, and others, collectively called Bachmann–Landau notation or asymptotic notation. Big O notation characterizes functions according to their growth rates: different functions with the same asymptotic growth rate may be represented using the same O notation. The letter O is used because the growth rate of a function is also referred to as the order of the function. In computer science, big O notation is used to classify algorithms according to how their run time or space requirements grow as the input size grows. A description of a function in terms of big O notation usually only provides an upper bound on the growth rate of the function.

## [Markov Chain](https://en.wikipedia.org/wiki/Markov_chain) or Markov Process

A Markov chain or Markov process is a [stochastic model](#stochastic-process-or-model) describing a sequence of possible events in which the probability of each event depends only on the state attained in the previous event. Informally, this may be thought of as, "What happens next depends only on the state of affairs now." A countably infinite sequence, in which the chain moves state at discrete time steps, gives a discrete-time Markov chain (DTMC). A continuous-time process is called a continuous-time Markov chain (CTMC). It is named after the Russian mathematician Andrey Markov.

A Markov process is a stochastic process that satisfies the Markov property (sometimes characterized as "memorylessness"). In simpler terms, it is a process for which predictions can be made regarding future outcomes based solely on its present state and—most importantly—such predictions are just as good as the ones that could be made knowing the process's full history.In other words, conditional on the present state of the system, its future and past states are independent.

Markov models are used to model changing systems. There are 4 main types of models, that generalize Markov chains depending on whether every sequential state is observable or not, and whether the system is to be adjusted on the basis of observations made:

Automous or Controlled | System state is fully observable | System state is partially observable
-----------------------|----------------------------------|-------------------------------------
System is autonomous   | Markov chain                     | Hidden Markov model
System is controlled   | Markov decision process          | Partially observable Markov decision process

## [hidden Markov Model](https://en.wikipedia.org/wiki/Hidden_Markov_model)

A hidden Markov model (HMM) is a statistical Markov model in which the system being modeled is assumed to be a Markov process (refered to as X X) with unobservable ("hidden") states. As part of the definition, HMM requires that there be an observable process Y Y whose outcomes are "influenced" by the outcomes of X X in a known way. Since X X cannot be observed directly, the goal is to learn about X X by observing Y . {\displaystyle Y.} HMM has an additional requirement that the outcome of Y Y at time t = t 0 {\displaystyle t=t_{0}} must be "influenced" exclusively by the outcome of X X at t = t 0 {\displaystyle t=t_{0}} and that the outcomes of X X and Y Y at t < t 0 {\displaystyle t<t_{0}} must be conditionally independent of Y Y at t = t 0 {\displaystyle t=t_{0}} given X X at time t = t 0 . {\displaystyle t=t_{0}.}

In its discrete form, a hidden Markov process can be visualized as a generalization of the urn problem with replacement (where each item from the urn is returned to the original urn before the next step). Consider this example: in a room that is not visible to an observer there is a genie. The room contains urns X1, X2, X3, ... each of which contains a known mix of balls, each ball labeled y1, y2, y3, ... . The genie chooses an urn in that room and randomly draws a ball from that urn. It then puts the ball onto a conveyor belt, where the observer can observe the sequence of the balls but not the sequence of urns from which they were drawn. The genie has some procedure to choose urns; the choice of the urn for the n-th ball depends only upon a random number and the choice of the urn for the (n − 1)-th ball. The choice of urn does not directly depend on the urns chosen before this single previous urn; therefore, this is called a Markov process.

## [Randomness](https://en.wikipedia.org/wiki/Randomness)

In common usage, randomness is the apparent or actual lack of definite pattern or predictability in information. A random sequence of events, symbols or steps often has no order and does not follow an intelligible pattern or combination. Individual random events are, by definition, unpredictable, but if the probability distribution is known, the frequency of different outcomes over repeated events (or "trials") is predictable.[note 1] For example, when throwing two dice, the outcome of any particular roll is unpredictable, but a sum of 7 will tend to occur twice as often as 4. In this view, randomness is not haphazardness; it is a measure of uncertainty of an outcome. Randomness applies to concepts of chance, probability, and information entropy.

## [Random Variable](https://en.wikipedia.org/wiki/Random_variable)

A random variable (also called random quantity, aleatory variable, or stochastic variable) is a mathematical formalization of a quantity or object which depends on random events. The term 'random variable' can be misleading as it is not actually random nor a variable, but rather it is a function from possible outcomes (e.g., the possible upper sides of a flipped coin such as heads H H and tails T T) in a sample space (e.g., the set { H , T } {\displaystyle \{H,T\}}) to a measurable space (e.g., { − 1 , 1 } \{-1,1\} in which 1 corresponding to H H and −1 corresponding to T T), often to the real numbers.

## [Sparse Matrix](https://en.wikipedia.org/wiki/Sparse_matrix)

In numerical analysis and scientific computing, a sparse matrix or sparse array is a matrix in which most of the elements are zero. There is no strict definition regarding the proportion of zero-value elements for a matrix to qualify as sparse but a common criterion is that the number of non-zero elements is roughly equal to the number of rows or columns. By contrast, if most of the elements are non-zero, the matrix is considered dense. The number of zero-valued elements divided by the total number of elements (e.g., m × n for an m × n matrix) is sometimes referred to as the sparsity of the matrix.

## [Stochastic Process](https://en.wikipedia.org/wiki/Stochastic_process) or Model

In probability theory and related fields, a stochastic or random process is a mathematical object usually defined as a sequence of random variables, where the index of the sequence has the interpretation of time. Stochastic processes are widely used as mathematical models of systems and phenomena that appear to vary in a random manner. Examples include the growth of a bacterial population, an electrical current fluctuating due to thermal noise, or the movement of a gas molecule.
