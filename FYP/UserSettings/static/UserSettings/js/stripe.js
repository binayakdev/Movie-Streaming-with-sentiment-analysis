var stripe = Stripe('pk_test_vo1sgnjwmkZCwbpFP3GVgwuX00PWNMsFKa');
var elements = stripe.elements();

var style = {
    base: {
        color: "#32325d",
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: "antialiased",
        fontSize: "16px",
        "::placeholder": {
            color: "#aab7c4"
        }
    },
    invalid: {
        color: "#fa755a",
        iconColor: "#fa755a"
    }
};

var cardElement = elements.create("card", { style: style });
cardElement.mount("#card-element");

var card = document.getElementById('card-element')

card.addEventListener('change', function (event) {
    var displayError = document.getElementById('card-errors');
    if (event.error) {
        displayError.textContent = event.error.message;
    } else {
        displayError.textContent = '';
    }
});

var form = document.getElementById('subscription-form');

form.addEventListener('submit', function (event) {
    // We don't want to let default form submission happen here,
    // which would refresh the page.
    event.preventDefault();

    stripe.createPaymentMethod({
        type: 'card',
        card: cardElement,
    }).then(function (result) {
        if (result.error) {
            var errorElement = document.getElementById('card-errors');
            errorElement.textContent = result.error.message;
            console.log(upgrade_button);
        } else {
            stripePaymentMethodHandler(result.paymentMethod.id)
        }
    });
});

function stripePaymentMethodHandler(result) {
    var hiddenInput = document.createElement('input')
    hiddenInput.setAttribute('type', 'hidden');
    hiddenInput.setAttribute('name', 'paymentMethod');
    hiddenInput.setAttribute('value', result);
    form.appendChild(hiddenInput);

    form.submit(); //Submitting the form
}