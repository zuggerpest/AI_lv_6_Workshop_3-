from rules import should_upsell
from logging_utils import log_experiment

def main():
    order_to_log = {"time_of_day": "lunch", "loyalty_member": "yes"}
    prediction = should_upsell(order_to_log)
    print("Prediction:", prediction)
    log_experiment(order_to_log, prediction, run_name="Initial Loyalty Rule")

if __name__ == "__main__":
    main()
