# Secrets Manager

- This allows you to pull secrets from your a secrets store

```pip
  pip3 install secretsmanager 
```

```python
  from secretsmanager.secretsmanager import SecretsManager
  sm = SecretsManager("arn:aws:secretsmanager:{region}:{aws_account}:secret:{secret_name}")
  print(sm.db_secret)
```
