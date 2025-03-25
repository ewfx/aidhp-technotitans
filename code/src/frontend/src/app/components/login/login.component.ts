import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
@Component({
  selector: 'app-login',
  imports: [CommonModule,FormsModule],  // Add necessary imports for the form here if needed
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  customerId: string = '';  
  password: string = '';     
  customers: { username: string, password: string }[] = [];

  constructor(private router: Router, private http: HttpClient) {}

  ngOnInit() {
    this.loadCustomerData();
  }

  // Fetch CSV data from Flask backend
  loadCustomerData() {
    this.http.get<{ username: string, password: string }[]>('http://localhost:5000/api/customers')
      .subscribe(
        (data) => { this.customers = data; },
        (error) => { console.error('Error fetching customer data:', error); }
      );
  }

login() {
  const user = this.customers.find(
    u => u.username.trim() === this.customerId.trim() && u.password.trim() === this.password.trim()
  );

  if (user) {
    localStorage.setItem('customerId', user.username);  // Store Customer ID
    this.router.navigateByUrl('/home');  // Navigate to Home
  } else {
    alert('Invalid Customer ID or Password! Please try again.');
  }
}

}
