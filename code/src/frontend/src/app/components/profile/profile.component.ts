import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { NavbarComponent } from "../navbar/navbar.component";
@Component({
  selector: 'app-profile',
  imports: [CommonModule, NavbarComponent],
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  customerId: string | null = null;
  customerData: any = null;

  constructor(private http: HttpClient, private route: ActivatedRoute) {}

  ngOnInit() {
    this.customerId = localStorage.getItem('customerId'); // Retrieve customer ID from localStorage

    if (this.customerId) {
      this.getCustomerDetails(this.customerId);
    }
  }

  getCustomerDetails(customerId: string) {
    this.http.get<any>(`http://localhost:5000/api/customer/${customerId}`).subscribe(
      (response) => {
        if (response.status === 'success') {
          this.customerData = response.data;
          delete this.customerData.Password; // Remove password for security
        }
      },
      (error) => {
        console.error('Error fetching customer details:', error);
      }
    );
  }
}