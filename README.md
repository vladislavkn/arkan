# arkan

Arkan is a simple python task runner. It helps you to run bash scripts in series or parallel.

## Example

```bash
series # This is a series group. Tasks inside it will be executed one-by-one
    echo 'Hello arkan!'
    parallel # This is a parallel group. Tasks inside it will be executed in parallel
        echo 'Boom! I am first'
        series # You can nest groups at any level!
            echo 'Nope!'
    echo 'finish'
```

