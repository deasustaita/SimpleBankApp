export interface ResponseEntity<T> {
    status_code: number;
    message: string;
    data: T | null;
}