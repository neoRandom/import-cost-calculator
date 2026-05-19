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

#### Details about Hexagonal Architecture

From start to finish, the development looks like this (in theory):

- What and how it should do (Use cases)
- What are the rules and the objects/entities (Models)
- What are, if any, the encapsulated single-responsibility business logic (Services)
- With what the user will interact with (Driver Adapters)
- How the service will use external services (Driven Adapters) (not present here)

DTOs are also included some times alongside the adapters, but never within the Domain.

That structure is not definitive and is very project-specific.

Forget about "hexagons", that name is misleading. The architecture is about services, interfaces/contracts/blueprints, and their implementations. The focus is in separation of contexts and responsibilities (not only business logic from infrastructure), related mainly by interfaces, and dependency inversion.

"Dependency inversion" means that if a part X is required by Y (e.g.: specific core is required by replaceable adapter), X needs to create an interface that Y will follow. Y depends on X, but X shouldn't even know that Y exists.

In general, and very oversimplified, the dependency flow goes like: driver adapter -> application / use cases -> service -> model. And the funny part is that the driven adapter can't be represented by a unidimensional flow, because it can be required by any of them: it's just there to fulfill an interface requirement, like the use case requiring somewhere to be save a model, or the service requiring some external device.

Driven adapters fulfill an external interface, because they will be injected as dependencies. Quite the opposite, driver adapters are dependent on interfaces and they don't have interfaces for themselves.

Generally, the abstraction goes with who will use it, so X will have the interface/contract for Y if it requires an implementation of Y. If the adapter requires a DTO, it will have one alongside itself (same file or folder), and so on.

As I said earlier, the focus is in separation of contexts, and dependency inversion, so everything here is just one of many ways of achieving a proper architecture for the project. Pure hexagonal architecture is bad because there are infinite cases where it may not fit perfectly, so the smartest way is not to follow it strictly, but rather understand the project to build an architecture that fits.
