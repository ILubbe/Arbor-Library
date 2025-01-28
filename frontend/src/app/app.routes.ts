import { Routes, RouterModule } from '@angular/router';
import { SignUpComponent } from './components/sign-up/sign-up.component';
import { LoginComponent } from './components/login/login.component';
import { HomeComponent } from './components/home/home.component';
import { Component } from '@angular/core';


export const routes: Routes = [
    {path:"", redirectTo:"login", pathMatch:"full"},
    {path:"sign-up", component:SignUpComponent},
    {path:"login", component:LoginComponent},
    {path:"home", component:HomeComponent}
];
export class AppComponent {}