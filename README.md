# Py VaultSimulator

VaultSimulator is a Python project for optimisation of a DEFI vault in which the rewards are earned in the native token. 
The specific vault used for this example was the BNB-AUTO LP, with a view to find the optimal amount of each harvest to maximise yield in different timeframes.

## Requirements

- Pandas only
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pandas.

```bash
pip install pandas
```

## Usage

To create a simulation object, we must use the Simulate class passing it the length of time in days in a start, stop, step format. 

```python
my_sim = Simulate((start, stop, step))
```

To test only the range of days with a set harvest target use:
```python
my_sim.test_X_numdays(start, stop, step)
```

To test only the range of harvest targets use with a set time length (changeable with AUTOBNBVault.change_default_days(new_num_days)):
```python
my_sim.test_x_harvest(start, stop, step)
```

To optimise for both simultaneously, we must pass both sets of paramters (in tuples) to optimise_harvest_days:
```python
my_sim.optimise_harvest_days((harvest_params), (days_params))
```

## Notes
This is designed as a semi-flexible calculator for a specific vault, with a view to create a more well-rounded interface should the need arise.

## License
[MIT](https://choosealicense.com/licenses/mit/)
