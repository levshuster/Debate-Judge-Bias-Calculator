# Usage Examples

```
$ scrape

A tool for Identifying probabamatic debate judges based on their tabroom records

Usage: scrape <COMMAND>

Commands:
  generate  Search tabroom to collect data
  analyze   Analyze a previously generated judge file
  view      View a previously generated judge file
  delete    Delete a previously generated judge file
  help      Print this message or the help of the given subcommand(s)

Options:
  -h, --help     Print help
  -V, --version  Print version
```

```
$ scrape --help
```
## Generate
```
$ scrape generate
Search tabroom to collect data

Usage: scrape generate <COMMAND>

Commands:
  judge       Collect data on a single judge
  judges      Collect data on a list of judges
  tournament  Collect data on a tournament
  help        Print this message or the help of the given subcommand(s)

Options:
  -h, --help  Print help
```

Scrape tabroom to generate a json file or a specified judge's record based on the judge's tabroom id.
<!-- write bash code exerpt -->
```
$ scrape generate judge --id 105729     # Lev Shuster's judging record
...

$ scrape generate judge --id 26867      # Laura Livingstons's judging record
...

$ scrape generate judge --id 26335      # Steve Rowe's judging record
...
```



Scrape tabroom to generate a json file or a specified judge's record based on the judge's First and last name. ***This method will error if there are multiple judges with the same name***
```
$ scrape generate judge --name "Lev Shuster"
...

$ scrape generate judge --name "Steven Helman"
...
```
## View
```
$ scrape view judge --name "Lev Shuster"
...

$ scrape view --short judge --name "Steven Helman"
```

## Analyze
```
$ scrape analyze judge
Interegate a judge

Usage: scrape analyze judge --name <NAME> <COMMAND>

Commands:
  gender  
  age     
  voting  
  help    Print this message or the help of the given subcommand(s)

Options:
  -n, --name <NAME>  Search tab room for a judge with a matching first and last name
  -h, --help         Print help
```

```
$ scrape analyze judge -n "Lev Shuster" gender --help
Usage: scrape analyze judge --name <NAME> gender [OPTIONS]

Options:
  -r, --hit-rate  Analyzise the ability of this program to guess debaters genders\
  -b, --ballance  analyze the ballance of vote for and against women
  -h, --help      Print help
  ...

```

```
$ scrape analyze judge -n "Lev Shuster" gender --hit-rate
of the 141 debaters, 2 are unknown
the api succsess rate is 98.58156%
```

```
$ scrape analyze judge -n "Laura Livingston" gender --ballance
the judge has given -10 more ballots to women than men
```

## Delete