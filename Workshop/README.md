# TOdooSports 🏟️

A fully integrated sports facility management ERP built on **Odoo 19**.  
Designed for multi-sport facility owners who need to manage courts, bookings, coaches, equipment, lockers, memberships, and dynamic pricing from a single backend system.

---

## 📋 Table of Contents

- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Features](#features)
- [Models](#models)
- [Installation](#installation)
  - [macOS](#macos)
  - [Windows](#windows)
- [Usage Flow](#usage-flow)
- [Technical Highlights](#technical-highlights)
- [Module Structure](#module-structure)

---

## Problem Statement

Running a sports facility in 2026 is more operationally complex than most people realise. A mid-sized padel or football club manages dozens of moving parts simultaneously — court schedules, coach availability, equipment stock, locker rentals, membership discounts, and peak-hour pricing — all of which directly affect revenue and customer experience.

Yet the vast majority of facility owners still rely on a combination of WhatsApp messages, paper notebooks, and basic spreadsheets to keep things running. The consequences are predictable and costly:

- **Double-bookings** are common because there is no single source of truth for court availability. A manager takes a booking over the phone while a staff member accepts the same slot on a walk-in basis.
- **Equipment disappears.** Rackets, bibs, and balls are handed out with no tracking system. There is no way to know how many are in circulation at any given moment, which means customers regularly get turned away because stock has run out.
- **Coaches are mismanaged.** Without a structured schedule, coaches get assigned to two courts at the same time, or a customer books a Padel lesson only to find out on arrival that the coach specialises in Football.
- **Pricing is flat and inflexible.** A court at 10 AM on a Tuesday is priced identically to a court at 8 PM on a Friday — the most in-demand slot of the week. Facility owners leave significant revenue on the table by failing to apply surge pricing during peak hours.
- **Maintenance is reactive, not proactive.** Courts are used until they break. There is no system to track accumulated usage hours, no threshold that triggers a maintenance flag, and no way to see at a glance which courts across a facility are operational.
- **Memberships are managed manually.** Discount entitlements are remembered informally, expiry dates are tracked in spreadsheets, and customers regularly receive discounts they are no longer entitled to — or are incorrectly denied discounts they have paid for.
- **Lockers generate passive income, but are never systematically tracked.** Monthly rentals expire without the owner knowing, and lockers sit rented-but-expired for weeks at a time.

The result is a business that is leaking revenue at every level — from pricing and equipment to staffing and memberships — while simultaneously delivering an inconsistent customer experience that drives members away.

---

## Solution

**TOdooSports** is a purpose-built sports facility management ERP that replaces the chaos of spreadsheets and informal systems with a single, fully integrated backend. Built on the Odoo 19 framework, it enforces business logic at the data layer — meaning rules are not just guidelines that staff can ignore, they are constraints that the system will not allow to be broken.

Every booking flows through a structured sport-first selection process. The system automatically filters facilities, courts, coaches, and equipment based on what the customer wants to play — eliminating mismatched bookings at the source. Pricing adjusts automatically based on the day and time. Membership discounts apply without any manual intervention. Courts flag themselves for maintenance when they reach their usage threshold. Equipment cannot be double-booked across concurrent sessions. And everything — from locker expiry to membership validity — is tracked in real time.

TOdooSports turns operational management from a daily firefight into a system that largely runs itself.

---

## Features

### 🏸 Sport-First Booking Flow
Bookings are guided step by step:
1. Select **Sport** (e.g. Padel, Football, Tennis)
2. Select **Facility** — filtered to only show facilities with courts for that sport
3. Select **Court** — filtered by sport and availability
4. Select **Coach** (optional) — filtered by sport and facility
5. Add **Equipment** — filtered by sport and facility
6. Select **Duration** — fixed slots of 1 to 5 hours

### 🏟️ Facility Management
- Manage multiple facilities with courts, coaches, equipment, and lockers
- Facility auto-suspends when all courts are under maintenance
- Facility reactivates automatically when a court becomes available
- Court maintenance tracking with usage threshold and accumulated hours
- Court auto-flips to maintenance when usage limit is reached
- "Mark as Repaired" button resets accumulated hours and restores availability

### 💰 Dynamic Pricing Engine
- Create pricing rules by day of week and time window
- Multiplier-based pricing (e.g. 1.5x on Friday evenings, 0.8x on Tuesday mornings)
- Pricing rule is auto-applied when booking start time is selected
- Applied rule name and multiplier shown on the booking for full transparency

### 👥 Membership System
- Create membership plans with discount percentage and annual fee
- Assign customers to plans via Membership Payments
- Membership activates immediately on payment creation
- Validity auto-set to 1 year from payment date
- Membership discount auto-applies to court cost on bookings
- Expired memberships tracked automatically via scheduled cron

### 🎽 Equipment Management
- Equipment linked to specific facility and sport type
- Real-time stock availability check across overlapping bookings at the same facility
- Equipment dropdown on bookings filtered by facility and sport
- Prevents double-booking of limited stock items across concurrent sessions

### 👨‍🏫 Coach Management
- Coaches linked to a facility and sport speciality
- Coach dropdown on bookings filtered by facility and sport
- Coach double-booking constraint — one coach, one court at a time
- Coach hourly fee added to booking total automatically

### 🔒 Locker Rental
- Lockers linked to facilities
- Small and Large locker types
- Renter and expiry date tracked per locker
- Auto-release of expired lockers via scheduled cron

### 🎫 Booking Management
- Overlap prevention across confirmed and draft bookings
- Maintenance threshold check before confirming a booking
- Membership expiry validation on booking creation
- Cancel booking with a single button
- Reset to draft from confirmed or cancelled states
- Full pricing breakdown: court cost, coach cost, equipment cost, discount, total

---

## Models

| Model | Description |
|---|---|
| `sports.type` | Dynamic sport types (Padel, Football, Tennis, etc.) |
| `sports.facility` | Facilities with courts, coaches, equipment, lockers |
| `sports.facility.court` | Courts with sport type, hourly rate, maintenance tracking |
| `sports.amenity` | Amenities assignable to courts via Many2many |
| `sports.coach` | Coaches linked to facility and sport |
| `sports.equipment` | Equipment linked to facility and sport with stock |
| `sports.equipment.line` | Equipment lines on bookings with stock validation |
| `sports.facility.booking` | Core booking model with full pricing logic |
| `sports.locker` | Locker rentals per facility with expiry tracking |
| `sports.membership` | Membership plans with discount and annual fee |
| `sports.membership.payment` | Payment records linking customers to plans |
| `sports.pricing.rule` | Day/time-based pricing multiplier rules |

---

## Installation

### Requirements

- Odoo 19
- Python 3.10+
- PostgreSQL 14+
- Git

---

### macOS

#### 1. Install dependencies

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and PostgreSQL
brew install python@3.11 postgresql git
brew services start postgresql
```

#### 2. Clone Odoo 19

```bash
mkdir ~/odoo && cd ~/odoo
git clone https://github.com/odoo/odoo.git --branch 19.0 --depth 1
```

#### 3. Create a virtual environment and install dependencies

```bash
cd ~/odoo
python3 -m venv venv
source venv/bin/activate
pip install -r odoo/requirements.txt
```

#### 4. Set up the database

```bash
createuser -s odoo
createdb odoo_db -O odoo
```

#### 5. Clone TOdooSports

```bash
mkdir -p ~/odoo/addons/workshop
git clone https://github.com/yourusername/todoo-sports.git ~/odoo/addons/workshop/sports
```

#### 6. Configure Odoo

Create `~/odoo/odoo.conf`:

```ini
[options]
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo
db_name = odoo_db
addons_path = /Users/yourusername/odoo/odoo/addons,/Users/yourusername/odoo/addons/workshop
```

#### 7. Install the module

```bash
source ~/odoo/venv/bin/activate
python3 ~/odoo/odoo/odoo-bin -c ~/odoo/odoo.conf -i sports
```

#### 8. Open in browser

```
http://localhost:8069
```

---

### Windows

#### 1. Install dependencies

- Download and install **Python 3.11** from https://www.python.org/downloads/
  - During installation check **"Add Python to PATH"**
- Download and install **PostgreSQL 18+** from https://www.postgresql.org/download/windows/
  - Note the password you set for the `postgres` user
- Download and install **Git** from https://git-scm.com/download/win

#### 2. Clone Odoo 19

Open **Command Prompt** or **PowerShell** as Administrator:

```bat
mkdir C:\odoo
cd C:\odoo
git clone https://github.com/odoo/odoo.git --branch 19.0 --depth 1
```

#### 3. Create a virtual environment and install dependencies

```bat
cd C:\odoo
python -m venv venv
venv\Scripts\activate
pip install -r odoo\requirements.txt
```

> If you get errors installing `psycopg2`, install the binary version instead:
> ```bat
> pip install psycopg2-binary
> ```

#### 4. Set up the database

Open **pgAdmin** (installed with PostgreSQL) or use **psql**:

```bat
"C:\Program Files\PostgreSQL\14\bin\psql.exe" -U postgres
```

Inside psql:

```sql
CREATE USER odoo WITH PASSWORD 'odoo';
CREATE DATABASE odoo_db OWNER odoo;
\q
```

#### 5. Clone TOdooSports

```bat
mkdir C:\odoo\addons\workshop
git clone https://github.com/yourusername/todoo-sports.git C:\odoo\addons\workshop\sports
```

#### 6. Configure Odoo

Create `C:\odoo\odoo.conf`:

```ini
[options]
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo
db_name = odoo_db
addons_path = C:\odoo\odoo\addons,C:\odoo\addons\workshop
```

#### 7. Install the module

```bat
cd C:\odoo
venv\Scripts\activate
python odoo\odoo-bin -c odoo.conf -i sports
```

#### 8. Open in browser

```
http://localhost:8069
```

> **Windows Firewall:** If the browser cannot connect, allow Python through Windows Firewall when prompted, or manually add a firewall rule for port 8069.

---

## Usage Flow

### Setting up a Facility

1. **Configuration → Sport Types** — add your sports (Padel, Football, Tennis, etc.)
2. **Configuration → Amenities** — add amenities (Showers, Parking, Changing Rooms, etc.)
3. **Facilities → New** — create a facility with a name and location
4. Inside the facility, add **Courts** with sport type, hourly rate, and usage threshold
5. Inside the facility, add **Coaches** with sport speciality and hourly fee
6. Inside the facility, add **Equipment** with sport type, stock quantity, and rental price
7. Inside the facility, add **Lockers** with type and monthly fee

### Setting up Pricing Rules

1. **Configuration → Pricing Rules → New**
2. Set day of week, start hour (24h format), end hour, and multiplier
3. Example: Friday, 18.0 to 23.0, multiplier 1.5 = 50% price increase on Friday evenings
4. Example: Tuesday, 6.0 to 12.0, multiplier 0.8 = 20% discount on Tuesday mornings

### Creating a Membership

1. **Memberships → Plans → New** — set plan name, discount %, and annual fee
2. **Memberships → Payments → New** — pick or create a customer, select plan, enter amount paid
3. Save — membership activates immediately and discount applies to all future bookings automatically

### Making a Booking

1. **Reservations → New**
2. Select customer → sport → facility → court
3. Optionally add a coach
4. Set start time and duration (1–5 hour fixed slots)
5. Add equipment from the Equipment tab if needed
6. Pricing breakdown auto-calculates with surge multiplier and membership discount applied
7. Save as Draft → Confirm → Mark as Done after the session completes

---

## Technical Highlights

- **`@api.depends` compute chains** — total price recalculates across court rate, coach fee, equipment subtotals, pricing multiplier, and membership discount in a single compute method
- **`@api.constrains`** — overlap detection, coach double-booking, equipment stock validation across concurrent bookings, maintenance threshold enforcement, membership expiry check, sport-facility-court matching validation
- **`@api.onchange`** — cascading field resets when sport, facility, or court changes to prevent mismatched selections reaching the database
- **`models.Constraint`** — database-level CHECK constraints on prices, stock quantities, and pricing multipliers
- **`ir.sequence`** — auto-generated booking references in `BK/YYYY/00001` format
- **`ir.cron`** — scheduled actions for automatic locker expiry release and membership expiry marking
- **`_inherit = 'res.partner'`** — extends the native Odoo contact model with membership plan, expiry date, and discount fields without modifying core code
- **Domain filters on views** — all dropdowns in the booking form are dynamically filtered based on upstream selections so users can never make a structurally invalid booking

---

## Module Structure

```
sports/
├── __init__.py
├── __manifest__.py
├── data/
│   ├── sequences.xml
│   └── cron.xml
├── models/
│   ├── __init__.py
│   ├── sports_amenity.py
│   ├── sports_type.py
│   ├── sports_facility.py
│   ├── sports_facility_court.py
│   ├── sports_coach.py
│   ├── sports_equipment.py
│   ├── sports_equipment_line.py
│   ├── sports_facility_booking.py
│   ├── sports_locker.py
│   ├── sports_membership.py
│   ├── sports_pricing_rule.py
│   └── res_partner.py
├── security/
│   └── ir.model.access.csv
└── views/
    ├── sports_amenity_views.xml
    ├── sports_type_views.xml
    ├── sports_facility_views.xml
    ├── sports_facility_court_views.xml
    ├── sports_coach_views.xml
    ├── sports_equipment_views.xml
    ├── sports_facility_booking_views.xml
    ├── sports_locker_views.xml
    ├── sports_membership_views.xml
    ├── sports_pricing_rule_views.xml
    └── sports_menus.xml
```

---

## Built With

- [Odoo 19](https://www.odoo.com) — ERP framework
- Python 3.11
- PostgreSQL 18
- XML (Odoo view architecture)

---

*Built for the TOdoo Buildathon 2026*
