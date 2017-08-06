import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { MaterialModule } from '@angular/material';

import { AboutComponent } from './about.component';
import { SubaboutComponent } from './comp/subabout/subabout.component';
import { NoaboutComponent } from './comp/noabout/noabout.component';

import { AuthGuard, ExAuthGuard } from 'app/service/guard.service';
const aboutRoutes: Routes = [
    {
        path: '',
        component: AboutComponent,
        canActivate: [ExAuthGuard],
        children: [
            { path: 'avatar', component: SubaboutComponent, canActivate: [ExAuthGuard] },
            { path: 'error', component: NoaboutComponent, canActivate: [AuthGuard] },
        ]
    }
]

@NgModule({
    imports: [
        CommonModule,
        MaterialModule,
        FormsModule,
        RouterModule.forChild(aboutRoutes),
    ],
    declarations: [
        AboutComponent,
        SubaboutComponent,
        NoaboutComponent
    ]
})
export class AboutModule { }
