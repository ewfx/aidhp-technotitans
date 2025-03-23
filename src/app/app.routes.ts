import { Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { HomeComponent } from './components/home/home.component';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' }, // Default route to login page
  { path: 'login', component: LoginComponent }, // Login page
  { path: 'home', component: HomeComponent} // Main app after login
];
