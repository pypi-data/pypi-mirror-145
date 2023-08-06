# turboparse

Parse TURBOMOLE output files into json outputs

## Example: command line

    turboparse output.ref

## Example: from python

    import turboparse
    
    with open("output.ref") as f:
        turbomole_dict_output = turboparse.parse_turbo(f)
        print( "Excitation energy: ", turbomole_dict_output["egrad"]["excited_states"][0]["energy"])

## How to make your own parsers
