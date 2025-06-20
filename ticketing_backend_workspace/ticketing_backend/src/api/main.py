from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from jose import JWTError, jwt


# App metadata for OpenAPI /docs
app = FastAPI(
    title="Ticketing Backend API",
    description=(
        "Handles all business logic, data processing, "
        "and API endpoints for the ticketing system."
    ),
    version="1.0.0",
    openapi_tags=[
        {"name": "auth", "description": "User authentication endpoints"},
        {"name": "tickets", "description": "Ticket CRUD and management endpoints"},
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# === "Database" for demo (in-memory) ===
fake_users_db = {
    "alice": {
        "username": "alice",
        "full_name": "Alice Example",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "bob": {
        "username": "bob",
        "full_name": "Bob Example",
        "email": "bob@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": False,
    }
}


class User(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# === Simple Auth/JWT support ===
SECRET_KEY = "secret-for-demo"  # In production, replace with secure env var!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# PUBLIC_INTERFACE
def verify_password(plain_password, hashed_password):
    """Fake password verification. Replace with real hashing."""
    return plain_password == hashed_password.replace("fakehashed", "")


# PUBLIC_INTERFACE
def get_user(db, username: str):
    """Get UserInDB if exists."""
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None


# PUBLIC_INTERFACE
def authenticate_user(fake_db, username: str, password: str):
    """Authenticate user credentials against fake DB."""
    user = get_user(fake_db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# PUBLIC_INTERFACE
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generates JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# PUBLIC_INTERFACE
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=username)
    if user is None:
        raise credentials_exception
    return user


# PUBLIC_INTERFACE
async def get_current_active_user(
    current_user: User = Depends(get_current_user),
):
    """Get active user or raise error if disabled"""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# ===== Authentication API Routes =====

# PUBLIC_INTERFACE
@app.post(
    "/auth/token",
    response_model=Token,
    tags=["auth"],
    summary="Get authentication token",
    description="Obtain a JWT access token for the user.",
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and return JWT Bearer token."""
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# PUBLIC_INTERFACE
@app.get(
    "/auth/me",
    response_model=User,
    tags=["auth"],
    summary="Get current user info",
)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Fetch details for the authenticated user."""
    return current_user


# ===== Ticket Models and DB =====
class TicketBase(BaseModel):
    title: str = Field(..., description="Summary or title of the ticket")
    description: str = Field(..., description="Detailed description")
    priority: Optional[str] = Field(
        default="normal", description="Priority (low/normal/high)"
    )
    assigned_to: Optional[str] = Field(
        default=None, description="Username assigned to"
    )


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[str] = None
    status: Optional[str] = None


class Ticket(TicketBase):
    id: int
    status: str = Field(
        default="open", description="Ticket status (open/closed)"
    )
    created_by: str
    created_at: datetime
    updated_at: datetime


tickets_in_db: Dict[int, Ticket] = {}
ticket_id_counter = 0


# === Utility ===
def get_next_ticket_id():
    global ticket_id_counter
    ticket_id_counter += 1
    return ticket_id_counter


# ===== Ticket Endpoints =====

# PUBLIC_INTERFACE
@app.post(
    "/tickets/",
    response_model=Ticket,
    status_code=201,
    tags=["tickets"],
    summary="Create new ticket",
)
async def create_ticket(
    ticket: TicketCreate, current_user: User = Depends(get_current_active_user)
):
    """Create and persist a new support ticket."""
    ticket_id = get_next_ticket_id()
    now = datetime.utcnow()
    new_ticket = Ticket(
        id=ticket_id,
        title=ticket.title,
        description=ticket.description,
        priority=ticket.priority or "normal",
        assigned_to=ticket.assigned_to,
        status="open",
        created_by=current_user.username,
        created_at=now,
        updated_at=now,
    )
    tickets_in_db[ticket_id] = new_ticket
    return new_ticket


# PUBLIC_INTERFACE
@app.get(
    "/tickets/",
    response_model=List[Ticket],
    tags=["tickets"],
    summary="List all tickets",
)
async def list_tickets(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_active_user),
):
    """Return a list of all tickets."""
    all_tickets = list(tickets_in_db.values())
    return all_tickets[skip: skip + limit]


# PUBLIC_INTERFACE
@app.get(
    "/tickets/{ticket_id}",
    response_model=Ticket,
    tags=["tickets"],
    summary="Get ticket details",
)
async def get_ticket(
    ticket_id: int, current_user: User = Depends(get_current_active_user)
):
    """Get ticket information by ID."""
    ticket = tickets_in_db.get(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


# PUBLIC_INTERFACE
@app.put(
    "/tickets/{ticket_id}",
    response_model=Ticket,
    tags=["tickets"],
    summary="Edit ticket",
)
async def update_ticket(
    ticket_id: int,
    update: TicketUpdate,
    current_user: User = Depends(get_current_active_user),
):
    """Edit ticket details including status, priority, assignment and text."""
    ticket = tickets_in_db.get(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if (
        ticket.created_by != current_user.username
        and ticket.assigned_to != current_user.username
    ):
        raise HTTPException(
            status_code=403, detail="You do not have permission to edit this ticket"
        )
    for field, value in update.dict(exclude_unset=True).items():
        setattr(ticket, field, value)
    ticket.updated_at = datetime.utcnow()
    tickets_in_db[ticket_id] = ticket
    return ticket


# PUBLIC_INTERFACE
@app.put(
    "/tickets/{ticket_id}/close",
    response_model=Ticket,
    tags=["tickets"],
    summary="Close ticket",
)
async def close_ticket(
    ticket_id: int, current_user: User = Depends(get_current_active_user)
):
    """Close a ticket (status to 'closed'). Only creator or assigned can close."""
    ticket = tickets_in_db.get(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if ticket.status == "closed":
        raise HTTPException(status_code=400, detail="Ticket already closed")
    if (
        ticket.created_by != current_user.username
        and ticket.assigned_to != current_user.username
    ):
        raise HTTPException(
            status_code=403, detail="You do not have permission to close this ticket"
        )
    ticket.status = "closed"
    ticket.updated_at = datetime.utcnow()
    tickets_in_db[ticket_id] = ticket
    return ticket


# PUBLIC_INTERFACE
@app.get(
    "/",
    tags=["misc"],
    summary="Health check endpoint",
)
def health_check():
    """Health check endpoint for system liveness."""
    return {"message": "Healthy"}


# --- NOTE: This is an in-memory DB & fake auth for PoC/demo. ---
# Replace with actual DB and production logic for real deployment.
