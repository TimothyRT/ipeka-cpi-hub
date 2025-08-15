# IPEKA CPI Parent's Hub

## DOMCloud deployment recipe

```yaml
features:
  - 'python 3.11.4'
  - mysql
  - ssl
  - 'ssl always'
source: 'https://github.com/TimothyRT/api-employee-photos'
nginx:
  root: public_html/app/static
  passenger:
    enabled: 'on'
    app_env: development
    app_root: public_html
    app_type: python
    startup_file: server.py
    python: .pyenv/shims/python
    env_var_list:
      - PYTHONDONTWRITEBYTECODE=1
commands:
  - 'cp .env.example .env'
  - 'pip install -r requirements.txt'
  - 'echo "application = app" >> server.py'
```

## References

* https://developers.google.com/workspace/guides/create-project
* https://drive.google.com/drive/folders/1ZiiYq3aQudiNY6jyh7Uf0L1RyDKY8i-h
* https://huggingface.co/spaces/not-lain/background-removal
* https://huggingface.co/spaces/ksvmuralidhar/face_detection
