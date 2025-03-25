import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';

export interface TransactionData {
  total_spent: number;
  total_transactions: number;
  category_spending: { [key: string]: number };
  loan_payments: { [key: string]: number };
}

@Injectable({
  providedIn: 'root'
})
export class TransactionService {
  // Update this to your actual backend URL
  private apiUrl = 'http://localhost:5000/customer-transactions';

  constructor(private http: HttpClient) {}

  getCustomerTransactions(customerId: string): Observable<TransactionData> {
    console.log('Fetching transactions for Customer ID:', customerId);
    return this.http.get<TransactionData>(`${this.apiUrl}/${customerId}`).pipe(
      tap(data => {
        console.log('Received transaction data:', data);
      }),
      catchError(this.handleError)
    );
  }

  private handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
      // Client-side or network error
      console.error('Client-side error:', error.error.message);
    } else {
      // Backend returned an unsuccessful response code
      console.error(
        `Backend returned code ${error.status}, ` +
        `body was: ${JSON.stringify(error.error)}`
      );
    }
    // Return an observable with a user-facing error message
    return throwError(() => new Error('Something went wrong; please try again later.'));
  }
}