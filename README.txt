To run the project:

1. Clone the repository
git clone https://github.com/LumboIshinaja/netbox_test_automation.git

2. Create virtual environment
python -m venv venv
source venv/Scripts/activate

3. Install dependencies
pip install -r requirements.txt
playwright install

4. Set USERNAME and PASSWORD as environment variables (you can put any other value just make sure to have defined variables)
export USERNAME="milostest"
export PASSWORD="password"

Running tests:

1. Running all tests
pytest

2. Running specific group of tests (all markers listed in pytest.ini)
pytest -m {marker} 

3. Running tests with printed values in output (needed for test_zad_3_racks.py)
pytest -s -m racks

### Creator ###
Milos Jovanovic for MDS Informatički inženjering