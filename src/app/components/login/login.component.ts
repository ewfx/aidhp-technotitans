import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  imports: [CommonModule,FormsModule],  // Add necessary imports for the form here if needed
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  phoneNumber: string = '';  // For phone number input
  password: string = '';     // For password input

  constructor(private router: Router) {}

  // Login method
  login() {
    // Simple validation for the phone number and password
    const validPhoneNumber = '9095500053'; 
    const validPassword = 'pass123';   

    if (this.phoneNumber === validPhoneNumber && this.password === validPassword) {
      
      this.router.navigateByUrl('/home');
    } else {
      alert('Invalid phone number or password! Please try again.');
    }
  }
}
