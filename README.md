# GreenGardens 🌱
Sapling Storefront - For Nature

A web-based storefront application for selling premium saplings. Built with Flask and featuring a clean, responsive design.

## Features

- 🌳 Browse a catalog of various sapling types
- 📝 Detailed product information for each sapling
- 🛒 Shopping cart functionality
- 💳 Checkout process
- 📱 Responsive design for mobile and desktop

## Installation

1. Clone the repository:
```bash
git clone https://github.com/aniko04/GreenGardens.git
cd GreenGardens
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the Flask development server:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

1. Browse available saplings on the home page
2. Click on a sapling to view detailed information
3. Add saplings to your cart
4. Review your cart and adjust quantities
5. Proceed to checkout and complete your order

## Project Structure

```
GreenGardens/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── sapling_detail.html
│   ├── cart.html
│   ├── checkout.html
│   └── order_confirmation.html
└── static/
    └── css/
        └── style.css     # Stylesheet
```

## Available Saplings

The storefront features a variety of saplings including:
- Oak Sapling
- Maple Sapling
- Pine Sapling
- Cherry Blossom Sapling
- Willow Sapling
- Birch Sapling

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3
- **Session Management**: Flask sessions for cart functionality

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is open source and available for educational purposes.
