export interface Customer {
    _id: string;
    username: string;
    name: string;
    email: string;
    time_created: string;
}

export interface LoginCredentials {
    username: string;
    password: string;
}

export interface RegisterCustomerPayload {
    username: string;
    password: string;
    name: string;
    email: string;
}