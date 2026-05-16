# Decisions Record

Some conclusions that I had during the development of the project

#### CalculationResult in application instead of domain

My initial plan was to put CalculationResult on `domain/models.py`, but I learned that domain/models is for service-specific data structures. Placing CalculationResult in application is separating the results of the use case from the pure business logic.

#### CalculateUseCase being Generic instead of Abstract

The initial look of the CalculateUseCase family was "abstract parent; children that inherit and modify the behavior". To be able to modify the behavior, like the `execute`'s `case` argument type, I was thinking of using the Liskov Substitution Principle, but it soon throw typing errors.

The issue was misinterpretation. Liskov's Principle says that for any X class, we can interchangeably replace it for any given Y subclass of X. My thought was using a base type (ImportingCase) on the abstract class (CalculateUseCase), then using subclasses (e.g.: TraditionalImportingCase) on the concrete classes (e.g.: CalculateAllCasesUseCase), but the Principle says exactly the opposite.

When using an abstract class, we make a contract (interface) based on that same class, so the argument will by default be the one at the abstract class. That means that the code may pass an object without our expected methods and values.

My initial thought was to just use it as it is and then check for the subtype in runtime, but that solution wasn't good enough, because it lacked strict typing and confirmation within development.

That's when Generics comes handy, because they invert that dependency. Using the `typing` library, we can define a type bounded to our generic type, meaning that it accepts any subtype that inherits it. Applying it to our base class, and then passing it down to the subclasses explictly defining the desired subclass, we can have a strongly typed structure for our use cases without relying on a single type.
