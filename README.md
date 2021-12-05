# Securing-Credentials-using-BCRYPT-Algorithm

Flask-Bcrypt is a Flask extension that provides bcrypt hashing utilities. Bcrypt can expand what is called its Key Factor to compensate for increasingly more-powerful computers and effectively “slow down” its hashing speed. Changing the Key Factor also influences the hash output, so this makes Bcrypt extremely resistant to rainbow table-based attacks. The largest benefit of bcrypt is that, over time, the iteration count can be increased to make it slower allowing bcrypt to scale with computing power. We can diminish any benefits attackers may get from faster hardware by increasing the number of iterations to make bcrypt slower.

Setup:
- pip install virtualenv
- python -m venv project-name
- scripts>activate
- pip install -r requirements.txt
- Create  database  “login”  with table  “account” 
- run python app.py


