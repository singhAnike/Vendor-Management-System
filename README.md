# Vendor Management System with Performance Metrics

## Introduction
This Django project implements a Vendor Management System with performance metrics tracking. The system allows for the management of vendor profiles, tracking of purchase orders, and calculation of various vendor performance metrics.

## Core Features

### Vendor Profile Management
- **Model Design:** Vendor information, including name, contact details, address, and a unique vendor code.
- **API Endpoints:**
  - `POST /api/vendors/`: Create a new vendor.
  - `GET /api/vendors/`: List all vendors.
  - `GET /api/vendors/{vendor_id}/`: Retrieve a specific vendor's details.
  - `PUT /api/vendors/{vendor_id}/`: Update a vendor's details.
  - `DELETE /api/vendors/{vendor_id}/`: Delete a vendor.

### Purchase Order Tracking
- **Model Design:** Purchase order details, including PO number, vendor reference, order date, items, quantity, and status.
- **API Endpoints:**
  - `POST /api/purchase_orders/`: Create a purchase order.
  - `GET /api/purchase_orders/?vendor_id=vendor_id`: List all purchase orders with an option to filter by vendor.
  - `GET /api/purchase_orders/?po_id=po_id`:
  - `GET /api/purchase_orders/{po_id}/`: Retrieve details of a specific purchase order.
  - `PUT /api/purchase_orders/{po_id}/`: Update a purchase order.
  - `DELETE /api/purchase_orders/{po_id}/`: Delete a purchase order.

### Vendor Performance Evaluation
- **Metrics:** On-Time Delivery Rate, Quality Rating, Response Time, Fulfillment Rate.
- **Model Design:** Vendor model includes fields for performance metrics.
- **API Endpoints:**
  - `GET /api/vendors/{vendor_id}/performance`: Retrieve a vendor's performance metrics.

## Data Models
1. **Vendor Model:**
   - Fields: name, contact_details, address, vendor_code, on_time_delivery_rate, quality_rating_avg, average_response_time, fulfillment_rate.

2. **Purchase Order (PO) Model:**
   - Fields: po_number, vendor, order_date, delivery_date, items, quantity, status, quality_rating, issue_date, acknowledgment_date.

3. **Historical Performance Model:**
   - Fields: vendor, date, on_time_delivery_rate, quality_rating_avg, average_response_time, fulfillment_rate.

## Backend Logic
- **On-Time Delivery Rate:** Calculated on PO status change to 'completed'.
- **Quality Rating Average:** Updated upon completion of each PO with a provided quality rating.
- **Average Response Time:** Calculated on PO acknowledgment by the vendor.
- **Fulfillment Rate:** Calculated on any change in PO status.

## API Endpoint Implementation
- `GET /api/vendors/{vendor_id}/performance`: Retrieves calculated performance metrics for a specific vendor.
- `POST /api/purchase_orders/{po_id}/acknowledge`: Endpoint for vendors to acknowledge POs.

## Project Setup Instructions

### 1. Install Pipenv (if not already installed)
### 2. follow these instructions to run the application
```bash
# First you need to clone the repository
step- 1. git clone https://github.com/singhAnike/vendor-management-system.git

# Now you can install the pipenv if not already installed usign the following command
step-2.  pip install pipenv

# Now you need to activate a virtula invornment using the following command
step-3   pipenv shell

# Now you are all set to runing the application 
step-4  (i) # First you need to run the migration commands
            i.  -> python manage.py makemigrations 
            ii. -> python manage.py migrate
            
# now you can run the application using the following command
step-5   python manage.py runserver

