def format_currency(amount: int) -> str:
    """Hàm bổ trợ định dạng tiền tệ (e.g., 1000000 -> 1,000,000)."""
    return f"{amount:,}"


class BankAccount:
    # Class attributes (Thuộc tính dùng chung cho toàn bộ hệ thống)
    bank_name = "Vietcombank"
    transaction_fee = 2000

    def __init__(self, account_number: str, account_name: str):
        # Biến private ẩn (Encapsulation) bảo vệ dữ liệu gốc
        self.__account_number = account_number
        self.__account_name = ""
        self.__balance = 0  # Số dư mặc định bằng 0

        # Gọi setter để chuẩn hóa tên ngay khi khởi tạo
        self.account_name = account_name

    # --- PROPERTIES (Tính đóng gói) ---

    @property
    def account_number(self) -> str:
        """Chỉ cho phép đọc số tài khoản, không cho sửa."""
        return self.__account_number

    @property
    def balance(self) -> int:
        """Chỉ cho phép đọc số dư, ngăn chặn can thiệp thay đổi trực tiếp."""
        return self.__balance

    @property
    def account_name(self) -> str:
        """Đọc tên chủ tài khoản."""
        return self.__account_name

    @account_name.setter
    def account_name(self, name: str):
        """Bẫy dữ liệu 3: Chuẩn hóa dữ liệu đầu vào khi gán/cập nhật tên."""
        cleaned_name = name.strip()
        if not cleaned_name:
            print("Tên tài khoản không được để trống")
            return

        # Loại bỏ khoảng trắng thừa ở giữa và chuyển thành IN HOA
        words = cleaned_name.split()
        self.__account_name = " ".join(words).upper()

    # --- METHODS MANAGEMENT (Quản lý Phương thức) ---

    @staticmethod
    def validate_account_number(account_number: str) -> bool:
        """Kiểm tra số tài khoản đầu vào (Phải đúng 10 chữ số)."""
        return account_number.isdigit() and len(account_number) == 10

    @classmethod
    def update_transaction_fee(cls, new_fee: int):
        """Cập nhật phí giao dịch áp dụng toàn hệ thống."""
        if new_fee < 0:
            print("Phí giao dịch không được âm")
            print(f"Phí giao dịch hiện tại vẫn là {format_currency(cls.transaction_fee)} VND")
            return
        cls.transaction_fee = new_fee
        print(f"Đã cập nhật phí giao dịch toàn hệ thống thành {format_currency(new_fee)} VND")

    # --- INSTANCE METHODS (Nghiệp vụ tài khoản) ---

    def deposit(self, amount: int):
        """Bẫy dữ liệu 1: Kiểm tra số tiền nạp."""
        if amount <= 0:
            print("Số tiền giao dịch phải lớn hơn 0")
            return
        self.__balance += amount
        print(f"Nạp tiền thành công: +{format_currency(amount)} VND")

    def withdraw(self, amount: int):
        """Bẫy dữ liệu 1 & 2: Kiểm tra số tiền rút và số dư khả dụng."""
        if amount <= 0:
            print("Số tiền giao dịch phải lớn hơn 0")
            return

        total_deduction = amount + BankAccount.transaction_fee
        if self.__balance < total_deduction:
            print("Giao dịch thất bại. Số dư không đủ để thanh toán số tiền và phí giao dịch")
            return

        self.__balance -= total_deduction
        print(f"Rút tiền thành công: -{format_currency(amount)} VND")
        print(f"Phí giao dịch: {format_currency(BankAccount.transaction_fee)} VND")

    def display_info(self):
        """Hiển thị chi tiết thông tin tài khoản hiện hành."""
        print(f"Ngân hàng: {BankAccount.bank_name}")
        print(f"Số tài khoản: {self.__account_number}")
        print(f"Tên chủ tài khoản: {self.__account_name}")
        print(f"Số dư hiện tại: {format_currency(self.__balance)} VND")
        print(f"Phí giao dịch: {format_currency(BankAccount.transaction_fee)} VND")


# --- CLI MENU IMPLEMENTATION ---

def main():
    current_account = None

    while True:
        print("\n===== VIETCOMBANK DIGIBANK SIMULATOR =====")
        print("1. Mở tài khoản mới")
        print("2. Xem thông tin tài khoản")
        print("3. Giao dịch Nạp / Rút tiền")
        print("4. Cập nhật Tên chủ tài khoản")
        print("5. Đổi phí giao dịch hệ thống")
        print("6. Thoát chương trình")
        print("==========================================")

        choice = input("Chọn chức năng (1-6): ").strip()

        if choice == "1":
            print("\n--- MỞ TÀI KHOẢN MỚI ---")
            while True:
                acc_num = input("Nhập số tài khoản 10 chữ số: ").strip()
                if BankAccount.validate_account_number(acc_num):
                    break
                print("Số tài khoản không hợp lệ!")
                print("Số tài khoản phải gồm đúng 10 chữ số.")

            acc_name = input("Nhập tên chủ tài khoản: ")
            current_account = BankAccount(acc_num, acc_name)
            
            # Kiểm tra xem tên có bị rỗng/lỗi lúc khởi tạo hay không
            if current_account.account_name:
                print("Mở tài khoản thành công!")
                print(f"Số tài khoản: {current_account.account_number}")
                print(f"Tên chủ tài khoản: {current_account.account_name}")
            else:
                # Nếu nhập tên rỗng lúc đầu, reset đối tượng để bắt buộc làm lại
                current_account = None

        elif choice in ["2", "3", "4"]:
            # Bẫy dữ liệu 4: Kiểm tra sự tồn tại của tài khoản trước khi thao tác
            if current_account is None:
                print("\nHệ thống chưa có thông tin tài khoản")
                print("Vui lòng mở tài khoản ở Chức năng 1 trước.")
                continue

            if choice == "2":
                print("\n--- THÔNG TIN TÀI KHOẢN ---")
                current_account.display_info()

            elif choice == "3":
                print("\n--- GIAO DỊCH NẠP / RÚT TIỀN ---")
                print("1. Nạp tiền")
                print("2. Rút tiền")
                sub_choice = input("Chọn loại giao dịch (1-2): ").strip()

                try:
                    amount = int(input("Nhập số tiền giao dịch: ").strip())
                except ValueError:
                    print("Số tiền phải là số nguyên hợp lệ.")
                    continue

                if sub_choice == "1":
                    current_account.deposit(amount)
                elif sub_choice == "2":
                    current_account.withdraw(amount)
                else:
                    print("Lựa chọn không hợp lệ.")
                
                print(f"Số dư mới: {format_currency(current_account.balance)} VND")

            elif choice == "4":
                print("\n--- CẬP NHẬT TÊN CHỦ TÀI KHOẢN ---")
                new_name = input("Nhập tên mới: ")
                old_name = current_account.account_name
                current_account.account_name = new_name
                
                # Nếu cập nhật thành công (tên mới khác rỗng và đã thay đổi)
                if current_account.account_name and current_account.account_name != old_name:
                    print(f"Cập nhật thành công. Tên mới: {current_account.account_name}")

        elif choice == "5":
            print("\n--- ĐỔI PHÍ GIAO DỊCH HỆ THỐNG ---")
            print(f"Phí giao dịch hiện tại: {format_currency(BankAccount.transaction_fee)} VND")
            try:
                new_fee = int(input("Nhập phí giao dịch mới: ").strip())
                BankAccount.update_transaction_fee(new_fee)
            except ValueError:
                print("Mức phí phải là số nguyên hợp lệ.")

        elif choice == "6":
            print("\nCảm ơn bạn đã sử dụng Vietcombank Digibank!")
            break
        else:
            print("\nChức năng không hợp lệ. Vui lòng chọn lại từ 1-6.")


if __name__ == "__main__":
    main()
    