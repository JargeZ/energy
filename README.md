# Energy compare system
## Brief project description
A system for finding advantageous electricity supplier offers. On one side of the system, tariffs from different suppliers are stored, and on the other side, the consumption history of clients. Consumption can be recorded in detail or partially through reverse analysis of the payment bill issued by the supplier.
## Running the demo project
```shell
git clone https://github.com/JargeZ/energy
cd energy
docker compose up --build
```
And then go to: [http://127.0.0.1:8888/admin/](http://127.0.0.1:8888/admin/)

login: `demo`
password: `demo`

<img width="1332" alt="Screenshot 2024-04-07 at 8 25 50 pm" src="https://github.com/JargeZ/energy/assets/17633366/b1fd21dd-812a-4896-b3dd-41985697c6a3">


# Implementation notes

The implementation took 2 days and two approaches. The main challenge was to implement a flexible tariff storage system that could satisfy different markets and conditions (peak load, temporary, tariff ladders, etc.).

First, it should be noted that as a last resort, all calculation logic can be fully implemented on the database side, as PostgreSQL is a very powerful tool. It allows for many things even without plugins, up to recursive functions and stored procedures, and with plugins, its capabilities are limitless.

The current implementation, however, favors time-saving and uses an iterative approach, simplifying the code as much as possible whenever possible.

## First version
Initially, it was decided to store the "TariffConditions" entity in a single denormalized model, covering possible states with a field for condition type and constraints at the database level.

This was enough to implement the first draft using TDD, where the first blue energy bill was taken as test data. The implementation was done, and the tests passed successfully.

The first approach on the first day helped to understand which problems and inconveniences were crucial for implementation.

## Version 2 and problem-solving

### Consumption quantums and timeframes
Consumption data can be obtained either in detail down to the minute or very roughly, as in the case of reverse analysis of the bill.

The main problem when calculating consumption based on the tariff is to match the tariff and how many units were consumed because the consumption record can cover both off-peak and peak load periods, and not just once, if, for example, consumption data is for a week.

Therefore, it was decided not to work with the entire segment as a whole but to divide it into time quantums. A quantum is essentially the resolution of the system. Currently, it is constant but can be any.
```python
# possible dynamic for each customer/supplier
QUANTILE_SIZE = timedelta(minutes=1)
```
All time segments of energy consumption we know are divided into quanta of the specified size and fed as a stream into each tariff. Tariffs are activated/ignored on quanta and calculate consumption within themselves.

### Tariffs and activation
If in the first implementation we had a tariff entity and tariff.conditions, which contained conditions in different fields, then in the second version, each condition is normalized to such a structure:
```python
class ActivationRule():
    name # human readable name for reusing
    parameter # DATE | TIME | WEEKDAY | CONSUMED
    operator # EQ | IN | NOT_IN | BETWEEN | NOT_BETWEEN
    value: ConditionValue
```
<img width="878" alt="Screenshot 2024-04-07 at 9 17 28 pm" src="https://github.com/JargeZ/energy/assets/17633366/b05ab790-476e-4edf-b95a-36fbc3295793">

Each condition is easily extensible, both in terms of parameters it can point to and supported operators. Each parameter is a simple class that implements matching with it:
```python
class WeekdayRule(BaseConditionRuleHandler):
    def check_eq(self, quantile: Quantile, calculator: "CalculatorService") -> bool:
        weekday = quantile.date.isoweekday()
        return self.condition_value == weekday

    def check_in(self, quantile: Quantile, calculator: "CalculatorService") -> bool:
        weekday = quantile.date.isoweekday()
        return weekday in self.condition_value

    ...
```

Each tariff has a many-to-many relationship to these conditions, allowing for the reuse of common conditions and the creation of complex tariffs:
```python
class Tariff(models.Model):
    priority = models.IntegerField(default=0)
    activation_rules = models.ManyToManyField(ActivationRule, related_name="tariffs")

    ... # more fields
```
Thus, thanks to a set of rules that must be met to activate the tariff and its priority over all others, we pass each consumption quantum through the tariffs and use the highest priority one for which all activation rules have been met (empty rules with lower priority are used for basic tariffs).
<img width="1404" alt="Screenshot 2024-04-07 at 9 13 05 pm" src="https://github.com/JargeZ/energy/assets/17633366/28464317-2daf-4988-b5fb-377c89859b1f">
<img width="968" alt="Screenshot 2024-04-07 at 9 14 36 pm" src="https://github.com/JargeZ/energy/assets/17633366/5398d760-8db5-4c7c-a41d-3baeeeb2420c">


## Conclusion
The project is fully covered by unit tests, linters, and auto-formatters, pytest/black/flake8/mypy.

Full typed and the able to ensure a quality-gate at the CI/CD level.

Test cases can be viewed in the test folder, and calculations are displayed in the admin for each client across all suppliers for demonstration purposes.
<img width="888" alt="Screenshot 2024-04-07 at 9 25 04 pm" src="https://github.com/JargeZ/energy/assets/17633366/9ec86200-6e36-44d4-800b-8ba99ae73697">


