# dotcp
Copy your selected dotfiles to directory

## What is it?
As said, **dotcp** copies your _selected_ dotfiles to directory you indicated.
For example, `dotcp ~/awesome-dotifles/config/` will copy your selected dotfiles into `~/awesome-dotfiles/config/`.
How to _select_ dotfiles, you would ask? **dotcp** has it's own config. E.g:
```
i3
fish
alacritty
```
_(**dotcp**'s config file path should be `$XDG_CONFIG_HOME/dotcp/config`, but you can indicate it using `--config` option)_

Now, if you would run the previous command, **dotcp** will copy **i3**, **fish** and **alacritty** config directories into `~/awesome-dotfiles/config/`.

## Why?
Just wanted to have something similar to [this script](https://github.com/jieggii/dotfiles/blob/ed77dc9c0a5056cd00d9e647e6d55a1498783434/update.bash) but customizable and extensible.

## Installation
As any other shitty python program it can be easily installed via **pip**:
`pip install --user dotcp`

## Usage
At first just run **dotcp** without any flags, indicating destination directory that does not yet exist:
`dotcp destination-dir/`

Then, to update content of `destination-dir` you will have to use one of these flags: `--overwrite` or `--append`.
* `--overwrite` does the same thing as `rm -r destination-dir && dotcp destination-dir`
* `--append` appends your selected dotfiles into `destination-dir` saving its content

Examples:
* `dotcp --overwrite destination-dir/`
* `dotcp --append destination-dir/`