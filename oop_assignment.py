#!/usr/bin/env python3
"""
OOP Assignment

Activity 1: Design Your Own Class
- Base class: Device
- Subclass: Smartphone
- Demonstrates: attributes, methods, constructor (__init__), inheritance,
  encapsulation (protected/private-like attribute + property), and polymorphism (overridden methods)

Activity 2: Polymorphism Challenge
- Base class: Vehicle (abstract)
- Subclasses: Car, Bike, Plane (each defines move() differently)
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


# =========================
# Activity 1 — Device/Smartphone
# =========================

class Device:
    """Base device with encapsulated battery and common behavior."""
    def __init__(self, brand: str, model: str, battery_level: int = 100) -> None:
        self.brand = brand
        self.model = model
        # Encapsulation: store as "protected" (convention: single underscore)
        self._battery = max(0, min(100, int(battery_level)))

    @property
    def battery_level(self) -> int:
        """Read-only view of battery level (0..100)."""
        return self._battery

    def charge(self, amount: int) -> None:
        """Charge the device by `amount` %, clamped to 100."""
        self._battery = max(0, min(100, self._battery + int(amount)))

    def _drain(self, amount: int) -> None:
        """Drain battery internally by `amount` %, clamped to 0."""
        self._battery = max(0, self._battery - int(amount))

    def use(self, minutes: int) -> None:
        """Base usage drains 1% per 10 minutes."""
        drain = max(0, minutes // 10)
        self._drain(drain)

    def specs(self) -> str:
        """Return a generic descriptor (polymorphic)."""
        return f"{self.brand} {self.model} — Battery: {self.battery_level}%"

    def __str__(self) -> str:
        return self.specs()


class Smartphone(Device):
    """Smartphone extends Device with apps, number, and overridden behavior."""
    def __init__(self, brand: str, model: str, phone_number: str, battery_level: int = 100) -> None:
        super().__init__(brand, model, battery_level)
        self.phone_number = phone_number
        self.apps: List[str] = []

    def install_app(self, name: str) -> None:
        if name not in self.apps:
            self.apps.append(name)
            # installing an app drains a tiny bit
            self._drain(1)

    def call(self, number: str, minutes: int = 1) -> None:
        """Simulate a phone call; drains 1% per minute (min 1%)."""
        drain = max(1, minutes)
        self._drain(drain)

    # Polymorphism: override specs() with richer info
    def specs(self) -> str:
        app_count = len(self.apps)
        return (f"{self.brand} {self.model} (📱 {self.phone_number}) — "
                f"Apps: {app_count}, Battery: {self.battery_level}%")

    # Polymorphism: override use() to drain faster than a generic device
    def use(self, minutes: int) -> None:
        """Smartphones drain 1% per 5 minutes of active use."""
        drain = max(0, minutes // 5)
        self._drain(drain)


# =========================
# Activity 2 — Polymorphism with Vehicles
# =========================

class Vehicle(ABC):
    @abstractmethod
    def move(self) -> str:
        """Return a string describing movement (implemented by subclasses)."""
        raise NotImplementedError


class Car(Vehicle):
    def move(self) -> str:
        return "Driving 🚗"


class Bike(Vehicle):
    def move(self) -> str:
        return "Riding 🚲"


class Plane(Vehicle):
    def move(self) -> str:
        return "Flying ✈️"


# =========================
# Demo / Sample Usage
# =========================

def demo_activity_1() -> None:
    print("=== Activity 1 — Device / Smartphone ===")
    # Create unique objects with constructors
    d1 = Device("Acme", "Tab-10", battery_level=75)
    s1 = Smartphone("Pear", "iFruit 14", phone_number="+266-5012-3456", battery_level=65)
    s2 = Smartphone("Samesung", "Galaxy S42", phone_number="+266-5555-0000")

    # Use & mutate state via methods (encapsulation: battery managed internally)
    print(d1)  # uses Device.specs()
    d1.use(25)
    d1.charge(10)
    print("After use/charge:", d1)

    print(s1)  # uses Smartphone.specs() (polymorphism)
    s1.install_app("Maps")
    s1.install_app("Chat")
    s1.use(30)
    s1.call("+266-7777-8888", minutes=3)
    print("After installs/use/call:", s1)

    print(s2)
    s2.install_app("Music")
    print("Installed 'Music':", s2)

def demo_activity_2() -> None:
    print("\n=== Activity 2 — Polymorphism: Vehicles.move() ===")
    garage: List[Vehicle] = [Car(), Bike(), Plane()]
    for v in garage:
        # Late binding: the correct move() runs based on the actual object
        print(f"{v.__class__.__name__}: {v.move()}")

if __name__ == "__main__":
    demo_activity_1()
    demo_activity_2()
