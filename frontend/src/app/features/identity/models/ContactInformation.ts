export interface ContactInformation {
  email?: Email;
  phone_number?: Phonenumber;
  password?: Password;
}

interface Password {
  old_password: string;
  new_password: string;
  confirm_password: string;
}

interface Phonenumber {
  current_phone: string;
  new_phone: string;
  confirm_phone: string;
}

interface Email {
  current_email: string;
  new_email: string;
  confirm_email: string;
}
