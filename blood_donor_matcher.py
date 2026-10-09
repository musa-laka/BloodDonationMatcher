from dataclasses import dataclass
from enum import Enum
import random


class BloodType(str, Enum):
    Aplus = "Aplus"
    Aminus = "Aminus"
    Bplus = "Bplus"
    Bminus = "Bminus"
    ABplus = "ABplus"
    ABminus = "ABminus"
    Oplus = "Oplus"
    Ominus = "Ominus"


@dataclass
class Donor:
    donor_id: int
    name: str
    address: str
    blood_group: BloodType
    contact: int


@dataclass
class Request:
    name: str
    address: str
    blood_group: BloodType
    contact: int


donors: list[Donor] = []
requests: list[Request] = []


def take_request(name: str, address: str, blood_group: BloodType, contact: int) -> None:
    requests.append(Request(name, address, blood_group, contact))


def accept_request(donor_id: int) -> None:
    for donor in donors:
        if donor.donor_id == donor_id:
            print(
                f"Donor Info: {donor.name}, {donor.address}, "
                f"{donor.blood_group.value}, contact: {donor.contact}"
            )
            return
    print("A donor with that ID doesn't exist.")


def add_donor(name: str, address: str, blood_group: BloodType, contact: int) -> None:
    donors.append(Donor(len(donors) + 1, name, address, blood_group, contact))


def get_distance(donor_address: str, request_address: str) -> int:
    return random.randint(1, 10)


def ask_blood_type() -> BloodType | None:
    while True:
        value = read_line(
            "Enter blood type (Aplus, Aminus, Bplus, Bminus, "
            "ABplus, ABminus, Oplus, Ominus):"
        )
        if value is None:
            return None
        try:
            return BloodType(value)
        except ValueError:
            print("Invalid blood type. Please try again.")


def can_donate_to(donor_type: BloodType, recipient_type: BloodType) -> bool:
    donor_group = donor_type.value.removesuffix("plus").removesuffix("minus")
    recipient_group = recipient_type.value.removesuffix("plus").removesuffix("minus")
    abo_compatible = (
        donor_group == "O"
        or donor_group == recipient_group
        or recipient_group == "AB"
    )
    rh_compatible = not donor_type.value.endswith("plus") or recipient_type.value.endswith("plus")
    return abo_compatible and rh_compatible


def read_line(prompt: str) -> str | None:
    try:
        return input(prompt).strip()
    except EOFError:
        return None


def read_number(prompt: str, allow_empty: bool = False) -> int | None:
    while True:
        value = read_line(prompt)
        if value is None or (allow_empty and not value):
            return None
        try:
            return int(value)
        except ValueError:
            print("Please enter a valid whole number.")


def handle_donation() -> None:
    name = read_line("Enter donor name:")
    address = read_line("Enter donor address:")
    if name is None or address is None:
        return

    blood_group = ask_blood_type()
    contact = read_number("Enter contact number:") if blood_group else None
    if blood_group is not None and contact is not None:
        add_donor(name, address, blood_group, contact)
        print(f"Donor added with ID {donors[-1].donor_id}.")


def handle_request() -> None:
    name = read_line("Enter recipient name:")
    address = read_line("Enter recipient address:")
    if name is None or address is None:
        return

    blood_group = ask_blood_type()
    contact = read_number("Enter contact number:") if blood_group else None
    if blood_group is None or contact is None:
        return
    take_request(name, address, blood_group, contact)

    matches = [donor for donor in donors if can_donate_to(donor.blood_group, blood_group)]
    for donor in matches:
        distance = get_distance(donor.address, address)
        print(
            f"Donor ID {donor.donor_id}: {donor.name} ({donor.blood_group.value}), "
            f"estimated distance: {distance} km"
        )

    if not matches:
        print("No compatible donors are currently available.")
        return

    donor_id = read_number("Enter donor ID to accept, or press Enter to skip:", allow_empty=True)
    if donor_id is None:
        return
    if any(donor.donor_id == donor_id for donor in matches):
        accept_request(donor_id)
    else:
        print("That donor is not in the compatible matches above.")


def main() -> None:
    while True:
        response = read_line("Donate or request? (press Enter to exit)")
        if response is None or not response:
            break
        response = response.lower()
        if response == "donate":
            handle_donation()
        elif response == "request":
            handle_request()
        else:
            print("Invalid response. Enter 'donate' or 'request'.")


if __name__ == "__main__":
    main()