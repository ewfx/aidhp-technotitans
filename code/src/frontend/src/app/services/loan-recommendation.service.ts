import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class LoanRecommendationService {
  private apiUrl = 'http://127.0.0.1:5000/recommend-loan'; // Flask API URL

  constructor(private http: HttpClient) {}

  getLoanRecommendation(customerId: string | null = ''): Observable<any> {
    return this.http.post<any>(this.apiUrl, { customer_id: customerId });
  }
}
