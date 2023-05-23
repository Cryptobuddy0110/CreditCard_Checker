import streamlit as st
import stripe

# Set your Stripe API keys
stripe.api_key = "sk_test_51NAX2nSAY6eA8GaVLzpkam1aXtNpcT0gVUJnhqc952w6nuPBanbGNw2VJRGGpk4pHj9pkSkdWNMkP6SVWz4CXw4T00wxgKt2bb"

def verify_card(card_number, exp_date, cvv_number):
    # Step 1: Validate card number using the Luhn algorithm
    is_luhn_valid = luhn_algorithm_validation(card_number)
    if not is_luhn_valid:
        return False, "Invalid card number."

    try:
        # Step 2: Create a PaymentMethod using the card details
        payment_method = stripe.PaymentMethod.create(
            type="card",
            card={
                "number": card_number,
                "exp_month": int(exp_date.split("/")[0].strip()),
                "exp_year": int(exp_date.split("/")[1].strip()),
                "cvc": cvv_number
            }
        )

        # Step 3: Check if the PaymentMethod is valid
        if payment_method.id:
            return True, ""
        else:
            return False, "Card verification failed."
    except stripe.error.CardError as e:
        # Handle specific card errors
        error = e.error
        return False, error.get("message", "An error occurred while processing the payment.")
    except stripe.error.StripeError as e:
        # Handle other Stripe-related errors
        error = e.error
        return False, "An error occurred while processing the payment."


def luhn_algorithm_validation(card_number):
    card_number = str(card_number)
    checksum = 0
    num_digits = len(card_number)
    odd_even = num_digits & 1

    for i in range(num_digits):
        digit = int(card_number[i])

        if not ((i & 1) ^ odd_even):
            digit *= 2
        if digit > 9:
            digit -= 9

        checksum += digit

    return checksum % 10 == 0

def main():
    st.title("Credit Card Details")
    
    # Input fields
    card_number = st.text_input("Card Number")
    exp_date = st.text_input("Expiration Date (MM/YYYY)") 
    cvv_number = st.text_input("CVV Number")
    
    submitted = st.button("Submit")

    # Validate and submit the form
    if submitted:
        if len(card_number) != 16:
            st.error("Card number should have 16 digits.")
        elif not cvv_number.isdigit() or len(cvv_number) > 3:
            st.error("CVV number should be a 3-digit number or less.")
        elif len(exp_date.split("/")) != 2:
            st.error("Invalid expiration date format. Please use MM/YYYY.")
        else:
            # Verify the card details using Stripe API
            is_valid_card, error_message = verify_card(card_number, exp_date, cvv_number)

            if is_valid_card:
                st.balloons()
                st.success("Card details are correct!")
            else:
                st.error("Wrong card details.")
                st.error(error_message)

if __name__ == '__main__':
    main()