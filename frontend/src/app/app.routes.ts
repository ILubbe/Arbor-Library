import { Routes } from '@angular/router';
import { SignUpComponent } from './components/sign-up/sign-up.component';
import { LoginComponent } from './components/login/login.component';
import { HomeComponent } from './components/home/home.component';
import { LibrarianDashboardComponent } from './components/librarian-dashboard/librarian-dashboard.component';
import { authGuard } from './auth.guard';
import { roleGuard } from './role.guard';
import { InComponent } from './components/librarian-dashboard/in/in.component';
import { OutComponent } from './components/librarian-dashboard/out/out.component';
import { ManageInventoryComponent } from './components/librarian-dashboard/manage-inventory/manage-inventory.component';
import { ManageUsersComponent } from './components/librarian-dashboard/manage-users/manage-users.component';
import { CancelReservationsComponent } from './components/librarian-dashboard/cancel-reservations/cancel-reservations.component';
import { ReportsComponent } from './components/librarian-dashboard/reports/reports.component';

export const routes: Routes = [
    {path: "", redirectTo: "login", pathMatch: "full"},
    {path: "sign-up", component: SignUpComponent},
    {path: "login", component: LoginComponent},
    {path: "home", component: HomeComponent, canActivate: [authGuard]},

    {
        path:"librarian-dashboard",
        component:LibrarianDashboardComponent,
        canActivate:[authGuard, roleGuard],
    children: [
        {path: "in", component: InComponent, canActivate: [authGuard, roleGuard]},
        {path: "out", component: OutComponent, canActivate: [authGuard, roleGuard]},
        {path: "manage-inventory", component: ManageInventoryComponent, canActivate: [authGuard, roleGuard]},
        {path: "manage-users", component: ManageUsersComponent, canActivate: [authGuard, roleGuard]},
        {path: "cancel-reservations", component: CancelReservationsComponent, canActivate: [authGuard, roleGuard]},
        {path: "reports", component: ReportsComponent, canActivate: [authGuard, roleGuard]}
    ]}
];

export class AppComponent {}