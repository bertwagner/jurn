# jurn 📝🦄
A tool for logging work progress throughout the week. Features tags and pretty output. Log entries stored in a local sqlite database.

## Writing Entries

`jurn log -m 'Wrangled cats via lasso.'`

## Tagging

You can add tags to logs for hierarchical organization and display.

`jurn log -m 'Wrangled cats via lasso.' -t 'Physical Fitness'`

You can tab complete within the tag option. For example, if you typed in:

`jurn log -m 'Wrangled cats via lasso.' -t 'Physical <TAB>`

jurn would return the following bash-style autocomplete suggestions based on your history of previously used tags:

```
Physical Fitness
Physical Security
```

This helps ensure youre messages stay organized.

You can also have subcategories by tagging with `#`, e.g. 

`jurn log -m 'Wrangled cats via lasso.' -t 'Physical Fitness#Cardio'`

## Printing (to the screen)

`jurn print -d week`

Result:

```
2022-11-01 to 2022-11-07
  • Physical Fitness
    • Cardio
      • Wrangled cats via lasso.
    • Strength
      • New PR benching 2 mules.
  • Physical Security
    • Installed new locks on the doors.
    • Added storage to camera recording devices.
```

### Database

The jurn database is stored in the following location by default:

`~/.jurn/jurn.db`

You can override this with the `--db-path <folder path> --db-filename <filename>` options.

### More Commands

Use `jurn --help` to view all available options.


